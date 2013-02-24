:: Parce que le shell Windows est trop ortho
:: pour pouvoir faire plusieurs commandes en une
:: ligne tout seul
@echo off

cd ..\\xml-server\\
passerelle2.exe %1 %2
cd ..\\server\\