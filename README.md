# TaxPilot

Agente de asesoría en **Public Country-by-Country Reporting** (Directiva (UE) 2021/2101 y transposiciones nacionales) para consultores de fiscalidad internacional.

Funciona como un espacio de trabajo de Claude Code: las instrucciones del agente están en `CLAUDE.md` y el conocimiento normativo en `corpus/`.

## Estructura

| Carpeta | Contenido |
|---|---|
| `corpus/` | Fuentes oficiales (PDF) + `index.yaml` con metadatos de cada norma |
| `clientes/` | Documentos recibidos de clientes (Excel, Word, PDF...) para analizar |
| `entregables/` | Borradores generados (memos, informes, presentaciones) |
| `plantillas/` | Plantillas corporativas para los entregables |
| `scripts/` | Herramientas de análisis programático (p. ej. validador de Excel CbCR) |

## Uso típico

1. **Consulta normativa**: pregunta directamente en el chat («¿Qué plazo de publicación tiene una filial española de matriz estadounidense?»). El agente responde con citas a artículos concretos del corpus.
2. **Análisis de fichero de cliente**: deja el fichero en `clientes/` y pide el análisis. El agente lo abre con código y lo contrasta contra el art. 48 quater.
3. **Entregable**: pide el formato (Word, PPT, email HTML) y se genera en `entregables/` como borrador para revisión.

## Aviso

Los outputs son borradores de apoyo generados con IA. Siempre requieren revisión de un profesional cualificado antes de su envío a cliente.
