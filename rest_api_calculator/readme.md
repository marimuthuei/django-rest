## Note
 - The application uses django rest framework for exposing the rest api and uses built-in browseable UI which can be opened in chrome browser for testing purpose.
 - The API report app uses RDBMS for tracking the request the mixin can be overridden to save the request in redis cache[RBS} which is more efficient in performing analytics
 - The Report table can be purged to keep the last 30 days
