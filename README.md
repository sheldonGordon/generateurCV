# GenerateurCV

Generateur de CV en PDF a partir d'un fichier de donnees YAML et de
templates HTML/Jinja2. Le programme produit quatre variantes A4, chacune
avec une mise en page distincte.

## Variantes disponibles

| Variante | Template | PDF genere |
|---|---|---|
| Classique | `template.html` | `CV_<NOM>_template.pdf` |
| Moderne | `template_moderne.html` | `CV_<NOM>_template_moderne.pdf` |
| Editorial | `template_editorial.html` | `CV_<NOM>_template_editorial.pdf` |
| Compacte | `template_compact.html` | `CV_<NOM>_template_compact.pdf` |

Dans chaque nom de fichier, les espaces du champ `infos.nom` sont remplaces
par des caracteres `_`.

## Prerequis

- Windows
- Python 3.12 ou plus recent
- wkhtmltopdf installe a l'emplacement suivant :
  `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`
- Une connexion internet uniquement pour installer les paquets Python

Le chemin wkhtmltopdf est actuellement fixe dans `build_cv.py`. Si
wkhtmltopdf est installe ailleurs, adaptez la variable `path_wkhtmltopdf`.

## Installation

Depuis la racine du projet :

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Avec `uv`, l'installation peut egalement etre lancee ainsi :

```powershell
uv sync
```

## Generation

Activer l'environnement virtuel si necessaire, puis lancer :

```powershell
python build_cv.py
```

Les quatre PDF sont crees a la racine du projet.

## Personnaliser le contenu

Modifier les valeurs dans [cv_data.yaml](cv_data.yaml). Le fichier est
charge avec l'encodage UTF-8.

Structure attendue :

```yaml
infos:
  nom: "Prenom NOM"
  titre: "Titre professionnel"
  accroche: "Resume professionnel"
  contact:
    email: "prenom.nom@example.com"
    telephone: "06 00 00 00 00"
    localisation: "Ville / Remote"
    github: "https://github.com/utilisateur"
    linkedin: "https://www.linkedin.com/in/utilisateur/"

competences:
  - categorie: "Categorie"
    items:
      - "Competence 1"
      - "Competence 2"

experiences:
  - poste: "Poste"
    entreprise: "Entreprise"
    periode: "Janvier 2026 - Present"
    contexte: "Contexte de la mission"
    realisations:
      - "Realisation 1"
      - "Realisation 2"

formations:
  - diplome: "Diplome"
    ecole: "Etablissement"
    annee: "2026"
```

Les sections `competences`, `experiences` et `formations` sont parcourues
comme des listes. Les champs attendus doivent donc etre conserves pour
permettre aux quatre templates de les afficher.

## Personnaliser les templates

Les fichiers `template*.html` utilisent Jinja2. Les donnees YAML sont
injectees sous l'objet `cv`. Exemple :

```html
<h1>{{ cv.infos.nom }}</h1>

{% for experience in cv.experiences %}
  <div>{{ experience.poste }} - {{ experience.entreprise }}</div>
{% endfor %}
```

Les templates sont automatiquement charges depuis la racine du projet.
Toute modification CSS ou HTML doit etre faite dans le template concerne.

Pour generer uniquement certains templates depuis un programme Python :

```python
from build_cv import generate_cv

pdfs = generate_cv([
    "template_moderne.html",
    "template_compact.html",
])
```

Sans argument, `generate_cv()` genere les quatre variantes.

## Fonctionnement

1. `build_cv.py` charge `cv_data.yaml`.
2. Jinja2 rend les templates HTML avec les donnees sous la forme `cv`.
3. pdfkit appelle wkhtmltopdf pour convertir le HTML en PDF.
4. Chaque fichier est ecrit a la racine du projet.

## Depannage

### `wkhtmltopdf.exe` introuvable

Verifier que wkhtmltopdf est bien installe dans :
`C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`.

Si une autre installation est utilisee, modifier
`path_wkhtmltopdf` dans [build_cv.py](build_cv.py).

### Module Python manquant

Verifier que l'environnement virtuel est active, puis relancer :

```powershell
python -m pip install -r requirements.txt
```

### Encodage ou caracteres accentues

Les fichiers YAML et HTML utilisent l'encodage UTF-8. Conserver cet
encodage pour les informations personnelles et les templates.
