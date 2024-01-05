""" JWT Authentication class. """

import logging

from django.contrib.auth import get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from edx_django_utils.cache import RequestCache
from edx_django_utils.monitoring import set_custom_attribute
from jwt import exceptions as jwt_exceptions
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from edx_rest_framework_extensions.auth.jwt.decoder import (
    configured_jwt_decode_handler,
    unsafe_jwt_decode_handler,
)
from edx_rest_framework_extensions.config import (
    ENABLE_FORGIVING_JWT_COOKIES,
    ENABLE_SET_REQUEST_USER_FOR_JWT_COOKIE,
    VERIFY_LMS_USER_ID_PROPERTY_NAME,
)
from edx_rest_framework_extensions.settings import get_setting


logger = logging.getLogger(__name__)


class JwtAuthenticationError(Exception):
    """
    Custom base class for all exceptions
    """


class JwtSessionUserMismatchError(JwtAuthenticationError):
    pass


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class JwtAuthentication(JSONWebTokenAuthentication):
    """
    JSON Web Token based authentication.

    This authentication class is useful for authenticating a JWT using a secret key. Clients should authenticate by
    passing the token key in the "Authorization" HTTP header, prepended with the string `"JWT "`.

    This class relies on the JWT_AUTH being configured for the application as well as JWT_PAYLOAD_USER_ATTRIBUTES
    being configured in the EDX_DRF_EXTENSIONS config.

    At a minimum, the JWT payload must contain a username. If an email address
    is provided in the payload, it will be used to update the retrieved user's
    email address associated with that username.

    Example Header:
        Authorization: JWT eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYzJiNzIwMTE0YmIwN2I0NjVlODQzYTc0ZWM2ODNlNiIs
        ImFkbWluaXN0cmF0b3IiOmZhbHNlLCJuYW1lIjoiaG9ub3IiLCJleHA.QHDXdo8gDJ5p9uOErTLZtl2HK_61kgLs71VHp6sLx8rIqj2tt9yCfc_0
        JUZpIYMkEd38uf1vj-4HZkzeNBnZZZ3Kdvq7F8ZioREPKNyEVSm2mnzl1v49EthehN9kwfUgFgPXfUh-pCvLDqwCCTdAXMcTJ8qufzEPTYYY54lY
    """

    def get_jwt_claim_attribute_map(self):
        """ Returns a mapping of JWT claims to user model attributes.

        Returns
            dict
        """
        return get_setting('JWT_PAYLOAD_USER_ATTRIBUTE_MAPPING')

    def get_jwt_claim_mergeable_attributes(self):
        """ Returns a list of user model attributes that should be merged into from the JWT.

        Returns
            list
        """
        return get_setting('JWT_PAYLOAD_MERGEABLE_USER_ATTRIBUTES')

    def authenticate(self, request):
        is_forgiving_jwt_cookies_enabled = get_setting(ENABLE_FORGIVING_JWT_COOKIES)
        # .. custom_attribute_name: is_forgiving_jwt_cookies_enabled
        # .. custom_attribute_description: This is temporary custom attribute to show
        #      whether ENABLE_FORGIVING_JWT_COOKIES is toggled on or off.
        #      See docs/decisions/0002-remove-use-jwt-cookie-header.rst
        set_custom_attribute('is_forgiving_jwt_cookies_enabled', is_forgiving_jwt_cookies_enabled)

        # .. custom_attribute_name: jwt_auth_result
        # .. custom_attribute_description: The result of the JWT authenticate process,
        #      which can having the following values:
        #        'n/a': When JWT Authentication doesn't apply.
        #        'success-auth-header': Successfully authenticated using the Authorization header.
        #        'success-cookie': Successfully authenticated using a JWT cookie.
        #        'forgiven-failure': Returns None instead of failing for JWT cookies. This handles
        #          the case where expired cookies won't prevent another authentication class, like
        #          SessionAuthentication, from having a chance to succeed.
        #          See docs/decisions/0002-remove-use-jwt-cookie-header.rst for details.
        #        'failed-auth-header': JWT Authorization header authentication failed. This prevents
        #          other authentication classes from attempting authentication.
        #        'failed-cookie': JWT cookie authentication failed. This prevents other
        #          authentication classes from attempting authentication.
        #        'user-mismatch-failure': JWT vs session user mismatch found for what would have been
        #          a forgiven-failure, but instead, the JWT failure will be final.
        #        'user-mismatch-enforced-failure': JWT vs session user mismatch found for what would
        #          have been a successful JWT authentication, but we are enforcing a match, and thus
        #          we fail authentication.

        is_authenticating_with_jwt_cookie = self.is_authenticating_with_jwt_cookie(request)
        try:
            user_and_auth = super().authenticate(request)

            # Unauthenticated, CSRF validation not required
            if not user_and_auth:
                set_custom_attribute('jwt_auth_result', 'n/a')
                return user_and_auth

            # Not using JWT cookie, CSRF validation not required
            if not is_authenticating_with_jwt_cookie:
                set_custom_attribute('jwt_auth_result', 'success-auth-header')
                return user_and_auth

            self.enforce_csrf(request)

            # CSRF passed validation with authenticated user

            # adds additional monitoring for mismatches; and raises errors in certain cases
            is_mismatch = self._is_jwt_cookie_and_session_user_mismatch(request)
            if is_mismatch and get_setting(ENABLE_SET_REQUEST_USER_FOR_JWT_COOKIE):
                raise JwtSessionUserMismatchError(
                    'Failing otherwise successful JWT authentication due to session user mismatch '
                    'with set request user.'
                )

            set_custom_attribute('jwt_auth_result', 'success-cookie')
            return user_and_auth

        except JwtSessionUserMismatchError as exception:
            # Warn against these errors because JWT vs session user should not be happening.
            logger.warning('Failed JWT Authentication due to session user mismatch.')
            # .. custom_attribute_name: jwt_auth_failed
            # .. custom_attribute_description: Includes a summary of the JWT failure exception
            #       for debugging.
            set_custom_attribute('jwt_auth_failed', 'Exception:{}'.format(repr(exception)))
            set_custom_attribute('jwt_auth_result', 'user-mismatch-enforced-failure')
            raise

        except Exception as exception:
            # Errors in production do not need to be logged (as they may be noisy),
            # but debug logging can help quickly resolve issues during development.
            logger.debug('Failed JWT Authentication.', exc_info=exception)

            exception_to_report = _deepest_jwt_exception(exception)
            set_custom_attribute('jwt_auth_failed', 'Exception:{}'.format(repr(exception_to_report)))

            if is_authenticating_with_jwt_cookie:
                # This check also adds monitoring details
                is_user_mismatch = self._is_jwt_cookie_and_session_user_mismatch(request)
                if is_forgiving_jwt_cookies_enabled:
                    if is_user_mismatch:
                        set_custom_attribute('jwt_auth_result', 'user-mismatch-failure')
                        raise
                    set_custom_attribute('jwt_auth_result', 'forgiven-failure')
                    return None
                set_custom_attribute('jwt_auth_result', 'failed-cookie')
                raise

            set_custom_attribute('jwt_auth_result', 'failed-auth-header')
            raise

    def authenticate_credentials(self, payload):
        """Get or create an active user with the username contained in the payload."""
        # TODO it would be good to refactor this heavily-nested function.
        # pylint: disable=too-many-nested-blocks
        username = payload.get('preferred_username') or payload.get('username')
        if username is None:
            raise exceptions.AuthenticationFailed('JWT must include a preferred_username or username claim!')
        try:
            user, __ = get_user_model().objects.get_or_create(username=username)
            attributes_updated = False
            attribute_map = self.get_jwt_claim_attribute_map()
            attributes_to_merge = self.get_jwt_claim_mergeable_attributes()
            for claim, attr in attribute_map.items():
                payload_value = payload.get(claim)

                if attr in attributes_to_merge:
                    # Merge new values that aren't already set in the user dictionary
                    if not payload_value:
                        continue

                    current_value = getattr(user, attr, None)

                    if current_value:
                        for (key, value) in payload_value.items():
                            if key in current_value:
                                if current_value[key] != value:
                                    logger.info(
                                        'Updating attribute %s[%s] for user %s with value %s',
                                        attr,
                                        key,
                                        user.id,
                                        value,
                                    )
                                    current_value[key] = value
                                    attributes_updated = True
                            else:
                                logger.info(
                                    'Adding attribute %s[%s] for user %s with value %s',
                                    attr,
                                    key,
                                    user.id,
                                    value,
                                )
                                current_value[key] = value
                                attributes_updated = True
                    else:
                        logger.info('Updating attribute %s for user %s with value %s', attr, user.id, payload_value)
                        setattr(user, attr, payload_value)
                        attributes_updated = True
                else:
                    if getattr(user, attr) != payload_value and payload_value is not None:
                        logger.info('Updating attribute %s for user %s with value %s', attr, user.id, payload_value)
                        setattr(user, attr, payload_value)
                        attributes_updated = True

            if attributes_updated:
                user.save()
        except Exception as authentication_error:
            msg = f'[edx-drf-extensions] User retrieval failed for username {username}.'
            logger.exception(msg)
            raise exceptions.AuthenticationFailed(msg) from authentication_error

        return user

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for Jwt cookie authentication.

        Copied from SessionAuthentication.
        See https://github.com/encode/django-rest-framework/blob/3f19e66d9f2569895af6e91455e5cf53b8ce5640/rest_framework/authentication.py#L131-L141  # noqa E501 line too long
        """
        check = CSRFCheck(get_response=lambda request: None)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

    @classmethod
    def is_authenticating_with_jwt_cookie(cls, request):
        """
        Returns True if authenticating with a JWT cookie, and False otherwise.
        """
        try:
            # If there is a token in the authorization header, it takes precedence in
            # get_token_from_request. This ensures that not only is a JWT cookie found,
            # but that it was actually used for authentication.
            request_token = JSONWebTokenAuthentication.get_token_from_request(request)
            cookie_token = JSONWebTokenAuthentication.get_token_from_cookies(request.COOKIES)
            return cookie_token and (request_token == cookie_token)
        except Exception:  # pylint: disable=broad-exception-caught
            return False

    def _is_jwt_cookie_and_session_user_mismatch(self, request):
        """
        Returns True if JWT cookie and session user do not match, False otherwise.

        Arguments:
            request: The request.

        Other notes:
        - If ENABLE_FORGIVING_JWT_COOKIES is toggled off, always return False.
        - Also adds monitoring details for mismatches.
        - Should only be called for JWT cookies.
        """
        # adds early monitoring for the JWT LMS user_id
        jwt_lms_user_id = self._get_and_monitor_jwt_cookie_lms_user_id(request)

        is_forgiving_jwt_cookies_enabled = get_setting(ENABLE_FORGIVING_JWT_COOKIES)
        # This toggle provides a temporary safety valve for rollout.
        if not is_forgiving_jwt_cookies_enabled:
            return False

        # If we set the request user in middleware for JWT auth, then we'd actually be checking JWT vs JWT user id.
        # Additionally, somehow the setting of request.user and the retrieving of request.user below causes some
        # unknown issue in production-like environments, and this allows us to skip that case.
        if _is_request_user_set_for_jwt_auth():
            # .. custom_attribute_name: skip_jwt_vs_session_check
            # .. custom_attribute_description: This is temporary custom attribute to show that we skipped the check.
            #      This is probably redundant with the custom attribute set_user_from_jwt_status, but temporarily
            #      adding during initial rollout.
            set_custom_attribute('skip_jwt_vs_session_check', True)
            return False

        wsgi_request = getattr(request, '_request', request)
        if wsgi_request == request:
            # .. custom_attribute_name: jwt_auth_with_django_request
            # .. custom_attribute_description: There exists custom authentication code in the platform that is
            #      calling JwtAuthentication with a Django request, rather than the expected DRF request. This
            #      custom attribute could be used to track down those usages and find ways to eliminate custom
            #      authentication code that lives outside of this library.
            set_custom_attribute('jwt_auth_with_django_request', True)

        # Get the session-based user from the underlying HttpRequest object.
        # This line taken from DRF SessionAuthentication.
        user = getattr(wsgi_request, 'user', None)
        if not user:  # pragma: no cover
            # .. custom_attribute_name: jwt_auth_request_user_not_found
            # .. custom_attribute_description: This custom attribute shows when a
            #      session user was not found during JWT cookie authentication. This
            #      attribute will not exist if the session user is found.
            set_custom_attribute('jwt_auth_request_user_not_found', True)
            return False

        if user.is_authenticated:
            session_lms_user_id = self._get_lms_user_id_from_user(user)
        else:
            session_lms_user_id = None

        if not session_lms_user_id or session_lms_user_id == jwt_lms_user_id:
            return False

        # .. custom_attribute_name: jwt_auth_mismatch_session_lms_user_id
        # .. custom_attribute_description: The session authentication LMS user id if it
        #      does not match the JWT cookie LMS user id. If there is no session user,
        #      or no LMS user id for the session user, or if it matches the JWT cookie user id,
        #      this attribute will not be included. Session authentication may have completed in middleware
        #      before getting to DRF. Although this authentication won't stick,
        #      because it will be replaced by DRF authentication, we record it,
        #      because it sometimes does not match the JWT cookie user.
        set_custom_attribute('jwt_auth_mismatch_session_lms_user_id', session_lms_user_id)

        return True

    def _get_and_monitor_jwt_cookie_lms_user_id(self, request):
        """
        Returns the LMS user id from the JWT cookie, or None if not found

        Notes:
        - Also provides monitoring details for mismatches.
        """
        try:
            cookie_token = JSONWebTokenAuthentication.get_token_from_cookies(request.COOKIES)
            invalid_decoded_jwt = unsafe_jwt_decode_handler(cookie_token)
            jwt_lms_user_id = invalid_decoded_jwt.get('user_id', None)
            jwt_lms_user_id_attribute_value = jwt_lms_user_id if jwt_lms_user_id else 'not-found'  # pragma: no cover
        except Exception:  # pylint: disable=broad-exception-caught
            jwt_lms_user_id = None
            jwt_lms_user_id_attribute_value = 'decode-error'

        # .. custom_attribute_name: jwt_cookie_lms_user_id
        # .. custom_attribute_description: The LMS user_id pulled from the
        #     JWT cookie. If the user_id claim is not found in the JWT, the attribute
        #     value will be 'not-found'. If the JWT simply can't be decoded,
        #     the attribute value will be 'decode-error'. Note that the id will be
        #     set in the case of expired JWTs, or other failures that can still be
        #     decoded.
        set_custom_attribute('jwt_cookie_lms_user_id', jwt_lms_user_id_attribute_value)

        return jwt_lms_user_id

    def _get_lms_user_id_from_user(self, user):
        """
        Returns the lms_user_id from the user object if found, or None if not found.

        This is intended for use only by LMS user id matching code, and thus will provide appropriate error
        logs in the case of misconfiguration.
        """
        # .. custom_attribute_name: jwt_auth_get_lms_user_id_status
        # .. custom_attribute_description: This custom attribute is intended to be temporary. It will allow
        #      us visibility into when and how the LMS user id is being found from the session user, which
        #      allows us to check the session's LMS user id with the JWT's LMS user id. Possible values include:
        #        - skip-check (disabled check, useful when lms_user_id would have been available),
        #        - not-configured (setting was None and lms_user_id is not found),
        #        - misconfigured (the property name supplied could not be found),
        #        - id-found (the id was found using the property name),
        #        - id-not-found (the property exists, but returned None)

        lms_user_id_property_name = get_setting(VERIFY_LMS_USER_ID_PROPERTY_NAME)

        # This special value acts like an emergency disable toggle in the event that the user object has an lms_user_id,
        # but this LMS id check starts causing unforeseen issues and needs to be disabled.
        skip_check_property_name = 'skip-check'
        if lms_user_id_property_name == skip_check_property_name:
            set_custom_attribute('jwt_auth_get_lms_user_id_status', skip_check_property_name)
            return None

        if not lms_user_id_property_name:
            if hasattr(user, 'lms_user_id'):
                # The custom attribute will be set below.
                lms_user_id_property_name = 'lms_user_id'
            else:
                set_custom_attribute('jwt_auth_get_lms_user_id_status', 'not-configured')
                return None

        if not hasattr(user, lms_user_id_property_name):
            logger.error(f'Misconfigured VERIFY_LMS_USER_ID_PROPERTY_NAME. User object has no attribute with name'
                         f' [{lms_user_id_property_name}]. User id validation will be skipped.')
            set_custom_attribute('jwt_auth_get_lms_user_id_status', 'misconfigured')
            return None

        # If the property is found, but returns None, validation will be skipped with no messaging.
        lms_user_id = getattr(user, lms_user_id_property_name, None)
        if lms_user_id:
            set_custom_attribute('jwt_auth_get_lms_user_id_status', 'id-found')
        else:  # pragma: no cover
            set_custom_attribute('jwt_auth_get_lms_user_id_status', 'id-not-found')

        return lms_user_id


_IS_REQUEST_USER_SET_FOR_JWT_AUTH_CACHE_KEY = '_is_request_user_for_jwt_set'


def set_flag_is_request_user_set_for_jwt_auth():
    """
    Sets a flag that the shows the request user was set to be based on JWT auth.

    Used to coordinate between middleware and JwtAuthentication. Note that the flag
    is stored in this module to avoid circular dependencies.
    """
    _get_module_request_cache()[_IS_REQUEST_USER_SET_FOR_JWT_AUTH_CACHE_KEY] = True


def is_jwt_authenticated(request):
    successful_authenticator = getattr(request, 'successful_authenticator', None)
    if not isinstance(successful_authenticator, JSONWebTokenAuthentication):
        return False
    if not getattr(request, 'auth', None):
        logger.error(
            'Unexpected error: Used JwtAuthentication, '
            'but the request auth attribute was not populated with the JWT.'
        )
        return False
    return True


def get_decoded_jwt_from_auth(request):
    """
    Grab jwt from request.auth in request if possible.

    Returns a decoded jwt dict if it can be found.
    Returns None if the jwt is not found.
    """
    if not is_jwt_authenticated(request):
        return None

    return configured_jwt_decode_handler(request.auth)


def _deepest_jwt_exception(exception):
    """
    Given an exception, traverse down the __context__ tree
    until you get to the deepest exceptions which is still
    a subclass of PyJWTError.  If no PyJWTError subclass
    exists, then just return the original exception.
    """
    relevant_exception = exception
    cur_exception = exception

    # An exception always has a context but if it's the deepest
    # exception, than __context__ will return None
    while cur_exception.__context__:
        cur_exception = cur_exception.__context__
        if isinstance(cur_exception, jwt_exceptions.PyJWTError):
            relevant_exception = cur_exception

    return relevant_exception


def _get_module_request_cache():
    return RequestCache(__name__).data


def _is_request_user_set_for_jwt_auth():
    """
    Returns whether the request user was set to be based on JWT auth in JwtAuthCookieMiddleware.

    This is a public method to enable coordination with the JwtAuthentication class.
    """
    return _get_module_request_cache().get(_IS_REQUEST_USER_SET_FOR_JWT_AUTH_CACHE_KEY, False)
