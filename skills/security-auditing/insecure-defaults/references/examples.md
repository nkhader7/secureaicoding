# Insecure Defaults: Examples and Counter-Examples

This document provides detailed examples for each vulnerability category, showing both vulnerable patterns (report these) and secure patterns (skip these).

## Fallback Secrets

### VULNERABLE - Report These

**Python: Environment variable with fallback**
```python
# File: src/auth/jwt.py
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

def create_token(user_id):
    return jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
```
**Why vulnerable:** App runs with known secret if `SECRET_KEY` is missing. Attacker can forge tokens.

**JavaScript: Logical OR fallback**
```javascript
// File: config/database.js
const DB_PASSWORD = process.env.DB_PASSWORD || 'admin123';
const pool = new Pool({ user: 'admin', password: DB_PASSWORD, database: 'production' });
```
**Why vulnerable:** Database accepts hardcoded password in production if env var missing.

### SECURE - Skip These

**Fail-secure: Crashes without config**
```python
SECRET_KEY = os.environ['SECRET_KEY']  # Raises KeyError if missing
```

**Explicit validation**
```javascript
if (!process.env.DB_PASSWORD) {
  throw new Error('DB_PASSWORD environment variable required');
}
```

---

## Default Credentials

### VULNERABLE - Report These

**Hardcoded admin account**
```python
def bootstrap_admin():
    if not User.query.filter_by(role='admin').first():
        admin = User(username='admin', password=hash_password('admin123'), role='admin')
        db.session.add(admin)
```
**Why vulnerable:** Default admin with known credentials created on first run.

**API key in code**
```javascript
const STRIPE_API_KEY = process.env.STRIPE_KEY || 'sk_test_...';
```

### SECURE - Skip These

```python
def bootstrap_admin():
    username = os.environ['ADMIN_USERNAME']
    password = os.environ['ADMIN_PASSWORD']
    # ...
```

---

## Fail-Open Security

### VULNERABLE - Report These

**Authentication disabled by default**
```python
REQUIRE_AUTH = os.getenv('REQUIRE_AUTH', 'false').lower() == 'true'

@app.before_request
def check_auth():
    if not REQUIRE_AUTH:
        return  # Skip auth check entirely
```

**CORS allows all origins**
```javascript
const allowedOrigins = process.env.ALLOWED_ORIGINS || '*';
app.use(cors({ origin: allowedOrigins }));
```

**Debug mode enabled by default**
```python
DEBUG = os.getenv('DEBUG', 'true').lower() != 'false'  # Default: true
```

### SECURE - Skip These

```python
REQUIRE_AUTH = os.getenv('REQUIRE_AUTH', 'true').lower() == 'true'  # Default: true
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'  # Default: false
```

---

## Weak Cryptography

### VULNERABLE - Report These

**MD5 for password hashing**
```python
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
```

**DES encryption**
```java
Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
```

**SHA1 for signature verification**
```javascript
const hmac = crypto.createHmac('sha1', WEBHOOK_SECRET);
```

### SECURE - Skip These

```python
# Non-security checksum (cache key generation)
def cache_key(data):
    return hashlib.md5(data.encode()).hexdigest()  # OK - not security-sensitive

# Password hashing with bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

---

## Permissive Access

### VULNERABLE - Report These

**World-writable files**
```python
fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o666)  # rw-rw-rw-
```

**S3 bucket public by default**
```python
bucket = s3.create_bucket(Bucket=name, ACL='public-read')
```

**CORS credentials with wildcard**
```python
response.headers['Access-Control-Allow-Origin'] = '*'
response.headers['Access-Control-Allow-Credentials'] = 'true'
```

### SECURE - Skip These

```python
fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o600)  # rw only owner
bucket = s3.create_bucket(Bucket=name, ACL='private')  # private by default
```

---

## Debug Features in Production

### VULNERABLE - Report These

**Stack traces in API responses**
```python
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': str(error),
        'traceback': traceback.format_exc()  # Leaks internals to attackers
    }), 500
```

**GraphQL introspection in production**
```javascript
const server = new ApolloServer({
  typeDefs, resolvers,
  introspection: true,   // Exposes full schema
  playground: true
});
```

**SQL errors exposed to users**
```java
catch (SQLException e) {
    return ResponseEntity.status(500).body(
        "Database error: " + e.getMessage()  // Reveals table names, constraints
    );
}
```

### SECURE - Skip These

```python
@app.errorhandler(Exception)
def handle_error(error):
    logger.exception('Request failed', exc_info=error)  # Logs full trace internally
    return jsonify({'error': 'Internal server error'}), 500  # Generic to user
```

```javascript
const server = new ApolloServer({
  typeDefs, resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  playground: process.env.NODE_ENV !== 'production'
});
```
