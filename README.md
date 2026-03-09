# TasaVe - Tasas de Cambio Venezuela

WebApp estática para visualizar tasas de cambio en Venezuela con calculadora reactiva bidireccional.

## 🚀 Características

- 📊 **Tasas en tiempo real**: BCV oficial (USD/EUR) y USDT (Binance P2P)
- 🧮 **Calculadora reactiva**: Conversión bidireccional entre VES, USD, EUR y USDT
- 🌓 **Modo oscuro/claro**: Diseño tipo app financiera con tema personalizable
- ⚡ **Actualización automática**: Los datos se actualizan cada hora vía GitHub Actions
- 📱 **Responsive**: Diseño mobile-first optimizado para todos los dispositivos

## 📋 Tecnologías

- **Frontend**: HTML5, Tailwind CSS, JavaScript vanilla
- **Backend**: Python 3.11 (scraping)
- **Hosting**: GitHub Pages
- **Automatización**: GitHub Actions

## 🛠️ Instalación local

### Prerrequisitos

- Python 3.11+
- pip

### Pasos

1. Clonar el repositorio:
```bash
git clone https://github.com/[tu-usuario]/paralelo_oficial_vzla.git
cd paralelo_oficial_vzla
```

2. Instalar dependencias de Python:
```bash
pip install -r requirements.txt
```

3. Ejecutar el scraper manualmente:
```bash
python scraper.py
```

4. Abrir `index.html` en tu navegador

## 📦 Deployment en GitHub Pages

1. Sube el repositorio a GitHub
2. Ve a **Settings** → **Pages**
3. Selecciona la rama `main` y carpeta `/` (root)
4. Guarda y espera el deployment
5. Tu app estará disponible en: `https://[tu-usuario].github.io/paralelo_oficial_vzla/`

## ⚙️ GitHub Actions

El workflow `.github/workflows/update.yml` se ejecuta automáticamente cada hora para:

1. Obtener tasas del BCV
2. Obtener precios USDT de Binance P2P
3. Generar `data.json` actualizado
4. Hacer commit y push si hay cambios

También puedes ejecutarlo manualmente desde la pestaña **Actions** en GitHub.

## 📊 Fuentes de datos

- **BCV (Banco Central de Venezuela)**: API pyDolarVenezuela (https://pydolarvenezuela-api.vercel.app/) para evitar errores 403.
- **Binance P2P**: API pública de anuncios P2P USDT/VES

## ⚠️ Importante

Los datos mostrados tienen carácter **exclusivamente informativo**. Esta aplicación no representa ni está afiliada a ninguna entidad gubernamental y no establece las tasas publicadas.

La única tasa oficial en Venezuela es la del BCV. El USDT P2P es solo una referencia estadística del mercado P2P internacional.

## 📝 Licencia

Este proyecto es de código abierto y está disponible solo con fines informativos.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.
