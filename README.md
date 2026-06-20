# Dashboard de Política de Inventario — Prototipo (Fase 1)

Más Delicias del Huila · Punto de venta Jardín Plaza · Diciembre 2024

## Qué incluye

- `app.py` — el dashboard (Streamlit)
- `requirements.txt` — librerías necesarias
- `data/` — datos ya calculados para este piloto:
  - `politica_productos.csv`: demanda, stock de seguridad y punto de reorden por producto
  - `politica_materiales.csv`: lo mismo, explotado a materias primas/insumos vía el BOM
  - `demanda_diaria.csv`: serie diaria de ventas por producto (diciembre 2024)
  - `match_articulos_bom.csv`: tabla de equivalencia entre nombre vendido y producto del BOM

## Cómo verlo funcionando (en tu computador)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre en tu navegador en `http://localhost:8501`.

## Cómo publicarlo gratis para verlo en el celular

1. Sube esta carpeta a un repositorio de GitHub (puede ser privado).
2. Entra a **share.streamlit.io** con tu cuenta de GitHub.
3. "New app" → selecciona el repo → archivo principal `app.py` → Deploy.
4. En unos minutos te da un link tipo `https://mdh-inventario.streamlit.app`.
   Ábrelo desde el navegador del celular — se ve bien sin instalar nada, sin costo,
   y sin límite de personas que lo consulten.

## Limitaciones de este prototipo (a resolver en la Fase 2)

- Solo cubre **32 de 91 productos** vendidos en diciembre — los que cruzaron con alta
  confianza por nombre contra el BOM. El resto necesita la tabla de equivalencias
  código histórico → código BOM que tu equipo está construyendo en Power Query.
- El **lead time** está fijo en 2 días para todos los materiales (provisional). En la
  Fase 2 se reemplaza por lead time real por proveedor.
- Los datos son estáticos (un mes ya cargado). En la Fase 2 se conecta a SharePoint
  para que se actualice solo cada noche después del cierre (9pm).
- El nivel de servicio en el panel de "Parámetros" es ilustrativo — conectarlo al
  cálculo real es uno de los siguientes pasos.

## Próximos pasos sugeridos

1. Conectar lectura automática de SharePoint (Microsoft Graph API) para ambos puntos
   de venta (Cosmocentro y Jardín Plaza).
2. Incorporar la tabla de equivalencias de códigos que tu equipo está depurando en
   Power Query, para subir la cobertura del 35% actual a ~100%.
3. Reemplazar el lead time fijo por los tiempos reales de cada proveedor.
4. Programar la actualización diaria con GitHub Actions (cron después del cierre).
