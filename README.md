# HBV301G – Verkefni 6: Endurskoðun virknikrafna

Endurskoðið **átta upphaflegar virknikröfur úr verkefni 1** samkvæmt
[verkefnislýsingunni](https://haskoliislands.instructure.com/courses/40813/pages/verkefni-6).
Beitið viðeigandi leiðbeiningum úr efni 12.1 og nýtið efni 11.1 við SRS-yfirlitið.
Endanlegur fjöldi krafna getur aukist ef samsettum kröfum er skipt upp.

## Gögn verkefnisins

| Staður | Innihald |
| --- | --- |
| Issues: eitt fyrir hverja upphaflega kröfu | Óbreyttur upphaflegur texti, uppruni, gæðamat og rökstuðningur |
| `requirements/<auðkenni>.md` | Gildandi krafa, tenging við issue, uppruni, SRS-staðsetning og prófunartilvik |
| [SRS-yfirlit.md](SRS-yfirlit.md) | Staðsetning allra krafna og tilvísanir í tengd gögn |
| Pull Requests | Efnisleg rýni, viðbrögð og samþykki |
| [reviews/PR-Comments.md](reviews/PR-Comments.md) | Tenglar í rýni og niðurstöður hennar |

Gildandi kröfutexti er í skránni. Issue geymir upphaflegan texta og ástæðu
breytingarinnar; Git-sagan varðveitir síðari breytingar á skránni.

## Vinnulag

1. Veljið saman átta upphaflegar kröfur og fyllið út hóptöfluna hér fyrir neðan.
   Skiptið ritun og rýni jafnt. Annar en höfundur rýnir hverja kröfu.
2. Stofnið eitt issue fyrir hverja valda kröfu með sniðmátinu **Yfirferð virknikröfu**.
   Afritið upphaflegan texta óbreyttan og tengið í verkefni 1. Greinið vandann og
   skráið hvaða leiðbeiningum úr 12.1 er beitt og hvernig þær bæta kröfuna.
   Greinið á milli orðalagsbreytingar og viðbættrar hegðunar eða forsendu.
   Ef orðalag er þegar gott má varðveita það með rökstuðningi.
3. Búið til grein, t.d. `feature/FR-03`. Afritið
   [requirements/FR-XX.md](requirements/FR-XX.md) í skrá sem heitir eftir auðkenni
   kröfunnar og fyllið út alla reiti. Varðveitið fyrirliggjandi auðkenni.
   Ef auðkenni vantar, úthlutið stöðugu auðkenni og skráið það líka í issue.
   Við uppskiptingu fá nýjar kröfur aðgreind auðkenni og tengingu við upphaflegu
   kröfuna. Þær mega fara í sama PR og tengjast sama yfirferðar-issue.
4. Skráið að minnsta kosti eitt prófunartilvik fyrir hverja gildandi kröfu:
   auðkenni prófs og kröfu, forsendur, upphafsástand, aðgerð/inntak og vænta niðurstöðu.
   Veljið auk þess **tvær kröfur** og bætið við undantekningar- eða jaðartilviki
   fyrir hvora. Ekki þarf að forrita eða keyra þessi prófunartilvik.
   Ef próf leiðir í ljós eyðu, uppfærið kröfuna og rökstuðning í issue.
5. Uppfærið SRS-yfirlitið. Merkið óútkljáð atriði `TBD` og skráið ábyrgðaraðila og
   næsta skref í issue. Ekki þarf að skila fullbúinni SRS-skýrslu.
6. Gerið commit og push og opnið eitt PR fyrir hverja upphaflega kröfu til `main`
   (eða sjálfgefinnar greinar safnsins). Notið lýsandi commit-skilaboð, t.d.
   `Endurbætt krafa FR-03: skýrari skilyrði og vænt niðurstaða`.
   Tengið PR við issue með `Closes #<númer>` og fyllið út PR-sniðmátið.
7. Opnið **Checks → Formathugun krafna** í PR. Lesið villuskilaboð, lagfærið og
   gerið nýtt commit og push í sama PR. Ný keyrsla þarf að standast.
8. Rýnir skrifar faglegar, nákvæmar og uppbyggjandi athugasemdir í PR við kröfuna
   og prófin, skráir hvað er vel gert og hvað þarf að bæta og uppfærir rýniyfirlitið
   á sömu grein. Höfundur bregst við og fær breytingar rýndar aftur.
   Þegar athuganir standast og annar en höfundur hefur samþykkt rýnina sameinar
   höfundur PR. Staðfestið að tengda issue-inu hafi verið lokað.

## Sjálfvirkar formathuganir

[GitHub Actions](.github/workflows/requirements.yml) keyrir við pull request,
push á `main` og handvirka keyrslu. Athugunin les öll Markdown-kröfuskjöl undir
`requirements/`, nema sjálft sniðmátið `requirements/FR-XX.md`.

Hún athugar skyldukafla og útfyllingu, samræmi auðkennis og skráarnafns,
GitHub-issue-tengil, tilvísun í SRS-yfirlit og prófunartilvik með einkvæmum
auðkennum og tengingu við rétta kröfu. Skiptið öllum `<...>` leiðbeiningareitum
út fyrir eigið efni. Haldið fyrirsögnum og heitum prófunarreita óbreyttum;
viðbótarkaflar eru leyfðir. Auðkenni mega innihalda bókstafi, tölur, bandstrik,
undirstrik og punkta og þurfa ekki að fylgja `FR-03` dæminu.

Athugunin metur ekki merkingu, gæði, aðgengi tengla, efni issue, fjölda upphaflegra
krafna, jaðartilvik fyrir tvær kröfur eða samþykki rýnanda. Þetta er hluti efnislegrar
rýni og lokayfirferðar. Tómt sniðmátssafn stenst með tilkynningu um að engar
útfylltar kröfur séu til staðar; það merkir ekki að verkefninu sé lokið.
`TBD` er leyfilegt þegar eftirfylgni er skráð í issue.

Keyra má sömu athugun með Python 3.10 eða nýrra, án aukapakka:

```sh
python scripts/check_requirements.py
```

Próf á hjálparforritinu: `python -m unittest discover -s scripts -p "test_*.py"`.
Þessi próf eru aðskilin frá skjalfestum prófunartilvikum nemenda.
Actions kemur ekki sjálfkrafa í veg fyrir merge. Eigandi safns getur valið
`Formathugun krafna` sem skylduathugun og krafist samþykkis í branch protection/ruleset.

## Hópur og verkaskipting

Tengill í safn verkefnis 1: <setjið inn tengil>

Fyllið út eina línu fyrir hverja af átta upphaflegu kröfunum; bætið við línum.

| Upphaflegt auðkenni / uppruni | Yfirferðar-issue | Gildandi auðkenni | Höfundur | Rýnir | PR |
| --- | --- | --- | --- | --- | --- |
| <krafa> | <tengill> | <auðkenni, einnig eftir uppskiptingu> | <nafn> | <annað nafn> | <tengill> |

## Lokayfirferð hóps

- [ ] Átta upphaflegar kröfur eiga hver sitt issue með óbreyttum texta, mati og rökstuðningi.
- [ ] Allar gildandi kröfur hafa stöðugt auðkenni, rekjanleika og prófunartilvik.
- [ ] Tvær kröfur hafa hvor sitt viðbótarpróf fyrir undantekningu eða jaðartilvik.
- [ ] SRS-yfirlit sýnir staðsetningu allra krafna og tengd gögn eða sýnilegar eyður.
- [ ] Allir hafa tekið þátt í ritun og efnislegri rýni; allar kröfur eru rýndar af öðrum en höfundi.
- [ ] Formathuganir standast og rýni er samþykkt áður en PR eru sameinuð.
