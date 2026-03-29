@echo off
:: Masuk ke folder temp relatif terhadap lokasi file bat
cd /d "%~dp0temp"

:: Menghapus semua file (termasuk mp4 dan m4a) tanpa bertanya (/q)
del /f /q *.*

:: Menghapus sub-folder jika ada
for /d %%x in (*) do rd /s /q "%%x"