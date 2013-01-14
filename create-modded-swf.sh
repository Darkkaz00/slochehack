cp $2 sloche_mod.swf
flasm -d sloche_mod.swf | sed s/www.sloche.com/$1/g | sed s/admin.sloche.com/$1/g > sloche_mod.asm
flasm -a sloche_mod.asm
mv sloche_mod.swf server/sloche-data/sloche.swf
rm sloche_mod.asm
rm -f sloche_mod.\$wf
