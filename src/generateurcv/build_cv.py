from pathlib import Path

import pdfkit
import yaml
from jinja2 import Environment, FileSystemLoader


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "cv_data.yaml"
TEMPLATE_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "output"
WKHTMLTOPDF = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

TEMPLATES = [
    "template.html",
    "template_moderne.html",
    "template_editorial.html",
    "template_compact.html",
]


def generate_cv(templates: list[str] | None = None) -> list[Path]:
    template_list = templates if templates is not None else TEMPLATES

    with DATA_FILE.open("r", encoding="utf-8") as data_file:
        data = yaml.safe_load(data_file)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF)
    options = {"encoding": "UTF-8"}

    base_name = data["infos"]["nom"].replace(" ", "_")
    generated_files: list[Path] = []
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for template_name in template_list:
        template = env.get_template(template_name)
        html_out = template.render(cv=data)

        variant = Path(template_name).stem
        output_pdf = OUTPUT_DIR / f"CV_{base_name}_{variant}.pdf"

        pdfkit.from_string(
            html_out,
            str(output_pdf),
            configuration=config,
            options=options,
        )
        generated_files.append(output_pdf)
        print(f"CV genere avec succes : {output_pdf}")

    return generated_files


def main() -> None:
    generate_cv()


if __name__ == "__main__":
    main()
