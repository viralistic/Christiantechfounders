export type Para = string | { quote: string } | { pull: string };

export interface PostSection {
  id: string;
  heading: string;
  paragraphs: Para[];
}

export interface Post {
  slug: string;
  title: string;
  lede: string;
  category: string;
  date: string;
  author: string;
  authorRole: string;
  authorInit: string;
  read: string;
  tags: string[];
  sections: PostSection[];
}

export const POSTS: Post[] = [
  {
    slug: 'waarom-we-stopten-met-open-gatherings',
    title: 'Waarom we gestopt zijn met grote open gatherings.',
    lede: 'Een lesson learned na de eerste anderhalf jaar van CTF, en wat we daarvan hebben overgehouden.',
    category: 'Reflecties',
    date: '12 Mei 2026',
    author: 'Marrallisa Kreijkes',
    authorRole: 'Founder en curator',
    authorInit: 'MK',
    read: '6 min lezen',
    tags: ['Strategy', 'Building', 'Community'],
    sections: [
      {
        id: 'het-begin',
        heading: 'Het begin: meer-is-beter.',
        paragraphs: [
          "Toen we CTF startten in 2025 dachten we, zoals veel community-initiatieven, dat het ging om mensen samenbrengen. Hoe meer hoe beter, hoe diverser hoe beter, hoe vaker hoe beter. Onze eerste gathering trok zo'n veertig mensen en het voelde als succes.",
          'Het werd ons in de loop van een paar maanden duidelijk dat het niet werkte. Het gemiddelde gesprek bleef oppervlakkig. Mensen kwamen met de verwachting van een netwerk-event en gingen weg met telefoonnummers die ze nooit gebruikten. De mensen die we het meest interessant vonden, kwamen één keer en niet meer.',
        ],
      },
      {
        id: 'wat-we-leerden',
        heading: 'Wat we hebben geleerd.',
        paragraphs: [
          'De fundamentele aanname onder grote open gatherings is dat schaal helpt. Dat klopt voor sommige dingen — netwerken, marktverkenning, vacatures — maar niet voor wat wij wilden, namelijk diepte. Diepte ontstaat in kleine kamers met scherpe mensen, niet in zalen met geïnteresseerde passanten.',
          { quote: 'We bouwden iets dat er goed uitzag. Het was alleen niet wat we eigenlijk wilden bouwen.' },
          'Sinds april 2026 werken we anders. Projecten in plaats van events. Op naam in plaats van open inschrijving. Kleinere groepen die om een vraagstuk samenkomen, en daarna verspreiden. Het voelt minder als community-werk en meer als curatie.',
        ],
      },
      {
        id: 'de-vorm',
        heading: 'De vorm die past.',
        paragraphs: [
          { pull: 'Klein zijn is geen tussenfase. Het is de vorm waarin het werk goed kan zijn.' },
          'De grootste verrassing was dat onze beste community-leden meteen reageerden. Ze hadden gewacht tot we deze keuze zouden maken. Wij dachten dat we onze community zouden verkleinen door minder open te zijn. In werkelijkheid hebben we hem geconcentreerd.',
          'Dat we daarvoor de meer-is-beter-aanname moesten loslaten, was de moeilijkste les. Maar ook de meest opluchtende.',
        ],
      },
      {
        id: 'wat-nu',
        heading: 'Wat dit voor jou betekent.',
        paragraphs: [
          'Als je dit leest en zelf een community bouwt: weet dat krimpen geen mislukking is. Vorm volgt functie. Een diepe groep verdraagt geen breed deelnemersveld, en een breed deelnemersveld verdraagt geen diep werk.',
          'We delen onze ervaringen graag uitgebreider tijdens projectdagen. Daar kan het gesprek gaan zoals het hoort: tussen mensen die elkaar kunnen volgen.',
        ],
      },
    ],
  },
  {
    slug: 'launch-platform-jongerenwerk',
    title: 'Launch: platform voor jongerenwerk in kleine kerken.',
    lede: 'We gingen live met een platform dat een stichting in Friesland zelf kan onderhouden, in één dag gebouwd.',
    category: 'Launch',
    date: '10 Apr 2026',
    author: 'Esther Vos',
    authorRole: 'Project lead',
    authorInit: 'EV',
    read: '4 min lezen',
    tags: ['Launch', 'Diaconaal', 'Open source'],
    sections: [
      {
        id: 'de-vraag',
        heading: 'De vraag.',
        paragraphs: [
          'Een stichting in Friesland coördineert jongerenwerk voor zes kleine kerken. Tot deze maand deden ze dat in een gedeelde spreadsheet. Met groei werd dat onhoudbaar.',
          'De vraag was niet "bouw een app", de vraag was "geef ons iets dat we zelf kunnen onderhouden, niet duurder is dan een seizoensbudget, en het probleem oplost binnen drie maanden".',
        ],
      },
      {
        id: 'in-een-dag',
        heading: 'In één dag.',
        paragraphs: [
          'Vijf bouwers op één locatie. We hebben de scope op de ochtend smal gemaakt: roosterbeheer, presentielijst, communicatie naar ouders.',
          { quote: 'De kunst was om niets te bouwen dat er over zes maanden niet meer kan zijn.' },
          'Tegen 16:30 hadden we een werkende versie. Tegen 19:00 had de stichting hem in handen.',
        ],
      },
      {
        id: 'wat-leeft-nu',
        heading: 'Wat leeft er nu.',
        paragraphs: [
          'Het platform draait op infrastructuur die de stichting bekostigt voor minder dan een tientje per maand. De code is open en gedocumenteerd. Twee leden van de stichting kunnen kleine aanpassingen zelf doen.',
          'Voor ons is dit het soort werk dat ertoe doet: klein, concreet, en in handen van mensen die er gebruik van maken.',
        ],
      },
    ],
  },
  {
    slug: 'ethiek-zonder-marketing',
    title: 'Wat ethiek is wanneer je het niet als marketing gebruikt.',
    lede: 'Een poging om te beschrijven hoe we naar productontwerp kijken zonder daar het verkoopargument van te maken.',
    category: 'Essays',
    date: '28 Apr 2026',
    author: 'Mark Visser',
    authorRole: 'Senior staff engineer',
    authorInit: 'MV',
    read: '9 min lezen',
    tags: ['Essay', 'Ethiek', 'Product'],
    sections: [
      {
        id: 'het-probleem',
        heading: 'Het probleem met "ethische AI".',
        paragraphs: [
          'Elke grote tech-organisatie heeft inmiddels een "responsible AI"-pagina. Bijna geen van die pagina\'s zegt iets wat het product anders maakt.',
          'Ethiek is op die manier marketing geworden: iets dat je communiceert, niet iets waarop je beslissingen verandert.',
        ],
      },
      {
        id: 'andere-aanpak',
        heading: 'Wat we proberen.',
        paragraphs: [
          'Bij CTF kijken we niet of een aanpak ethisch klinkt, maar of we hem zouden willen dat onze ouders, kinderen, of buren ermee in aanraking komen op een slechte dag.',
          { pull: 'Productontwerp is moreel ontwerp. Architectuur is ethische architectuur.' },
          'Dat is geen formele methode. Het is een dagelijkse vraag.',
        ],
      },
      {
        id: 'consequenties',
        heading: 'Wat dat in praktijk doet.',
        paragraphs: [
          'Soms bouwen we minder. Soms bouwen we iets dat trager groeit. Soms zeggen we nee tegen werk dat we technisch goed zouden kunnen doen.',
          'Dat is niet altijd het meest opportune. Het is wel waar we mee kunnen leven.',
        ],
      },
    ],
  },
];
