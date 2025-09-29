# FB-botV2
Cilj programa je, da iz skupine Dežurstva Študentski dom Ljubljana čim hitreje pobere vse proste termine ki se oddajajo.


## Kako uporabljati ta ful kul program?

1. V naprej si pripravi željeno Facebook skupino v Chromu.
2. Najprej si moraš naštimati pushBullet applikacijo na računalniku in telefonu in dobiti svoj api ključ ([https://www.pushbullet.com](Povezava))
3. Zaženi program in se prestavi na FB skupino v čim krajšem času.
4. Program bo pregledal če imaš vse potrebne knjižnice naložene in jih v nasprotnem primeru sam avtomatsko naložil.
5. Program bo periodično osveževal stran, dokler se v skupini ne pojavi novo sporočilo, ki vsebuje znakovni niz "odda".
6. Ko se pojavi novo sporočilo z določenim znakovnim nizom, bo program ali avtomatsko prevzel termin ali pa te o tem predhodno obvestil in počakal na tvojo potrditev preko aplikacije PushBullet.

POZOR! Ker se FB spletna stran pogosto spreminja mora biti uporabnik zelo previden da bot piše komentar na pravo mesto. (tle bi ful prav pršla integracija s Seleniumom (Terezija bo zih to zrihtala hmal)

## Kaj je še treba narediti in izboljšati

- Vse prevzete termine vstavi v nek koledar app.
- Program naj vzame samo termine, ki so v Rožni dolini (mora vsebovati pravo ime doma).
- Če želi nekdo menjati termin, mora napisati "Prevzamem če ne dobiš zamenjave :) ".
- Dodati je treba failsafe mehanizme oziroma nek reverse feedback loop, če gre kaj narobe, npr.: če začne internet štekat, če ima Facebook spletna stran probleme in tako naprej.
- zaznati mora "odda" in "Odda".


