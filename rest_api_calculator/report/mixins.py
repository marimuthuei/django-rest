from django.utils.timezone import now

from .models import APIRequestLog


class BaseAPILoggingMixin(object):

    def initial(self, request, *args, **kwargs):
        self.log = dict()
        self.log['requested_at'] = now()
        super(BaseAPILoggingMixin, self).initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        response = super(BaseAPILoggingMixin, self).handle_exception(exc)
        self.log['errors'] = response.data

        return response

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(BaseAPILoggingMixin, self).finalize_response(request, response, *args, **kwargs)

        self.log.update(
            {
                'api_name': self._get_api_name(request),
                'user': self._get_user(request),
                'latency': self._get_latency(),
                'status_code': response.status_code,
            }
        )
        try:
            self.save_log()
        except Exception:
            pass
        return response

    def save_log(self):
        raise NotImplementedError

    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None
        return user

    def _get_api_name(self, request):
        method = request.method.lower()
        try:
            attributes = getattr(self, method)
            api_name = type(attributes.__self__).api_name
            return api_name
        except AttributeError:
            return None

    def _get_latency(self):
        """
        Get the duration of the request response cycle is milliseconds.
        In case of negative duration 0 is returned.
        """
        response_timedelta = now() - self.log['requested_at']
        latency = int(response_timedelta.total_seconds() * 1000)
        return max(latency, 0)


class APILoggingMixin(BaseAPILoggingMixin):
    def save_log(self):
        """
        Api Logs are saved to database backend
        :return:
        """
        APIRequestLog(**self.log).save()


class APIRedisCaching(BaseAPILoggingMixin):
    """
    Redis cache server can be used to log the request and
    this can be more efficient than database logging
    """

    def save_log(self):
        raise NotImplementedError
