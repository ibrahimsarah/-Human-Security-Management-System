<!-- themes/university-theme/login/login.ftl -->
<!DOCTYPE html>
<html>
<head>
    <title>University System Login</title>
    <link rel="stylesheet" href="${url.resourcesPath}/css/login.css">
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <img src="${url.resourcesPath}/img/logo.png" alt="University Logo">
            <h1>University Management System</h1>
        </div>
        
        <form action="${url.loginAction}" method="post">
            <div class="form-group">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>