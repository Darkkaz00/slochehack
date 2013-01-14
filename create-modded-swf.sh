cp $2 sloche_mod.swf

# Reparation automatique d'un bogue etrange par rapport a Réal
# dans le client 2003. Voir la directoire patch2003 pour
# plus d'informations.
if [ "$(cat sloche_mod.swf | md5sum)" = "4fd90f12605dae1248382fa9416a80b4  -" ];
then
	echo "Patchage du bogue Real dans le client 2003..."
	cp sloche_mod.swf patch2003/
	cd patch2003
	mv sloche_mod.swf sloche2003.swf
	rm -f *flr*
	flasm -d sloche2003.swf >sloche2003.flr
	patch sloche2003.flr <patch-real-2003.diff
	cp sloche2003.swf sloche2003-fixreal.swf
	flasm -a sloche2003.flr
	rm -f *flr*
	mv sloche2003-fixreal.swf ../sloche_mod.swf
	rm -f *swf*
	rm -f *\$wf*
	cd ..
fi

flasm -d sloche_mod.swf | sed s/www.sloche.com/$1/g | sed s/admin.sloche.com/$1/g > sloche_mod.asm
flasm -a sloche_mod.asm
mv sloche_mod.swf server/sloche-data/sloche.swf
rm sloche_mod.asm
rm -f sloche_mod.\$wf
