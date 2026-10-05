# Database Setup Instructions

Please run the following commands in your PowerShell terminal to configure the MySQL database.

1. **Copy and configure the user script:**
   ```powershell
   Copy-Item springboot-backend\sql\create_user.sql springboot-backend\sql\create_user.local.sql
   ```
   *Now, open `springboot-backend\sql\create_user.local.sql` in your editor and replace `'CHANGE_ME'` with your secure password.*

2. **Execute the SQL scripts:**
   ```powershell
   cmd /c "mysql -u root -p < springboot-backend\sql\create_user.local.sql"
   ```
   *(Enter your root password when prompted)*

   ```powershell
   Remove-Item springboot-backend\sql\create_user.local.sql
   cmd /c "mysql -u root -p water_elixir < springboot-backend\sql\schema.sql"
   cmd /c "mysql -u root -p water_elixir < springboot-backend\sql\seed.sql"
   ```

3. **Verify the installation:**
   ```powershell
   cmd /c "mysql -u root -p water_elixir -e `"SHOW TABLES; SELECT * FROM zone;`""
   ```
   You should see exactly 5 tables (`alert`, `complaint`, `reading`, `ticket`, `zone`) and 4 zones.
