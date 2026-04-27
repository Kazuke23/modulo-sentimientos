import { useEffect } from "react"
import "../styles/Formulario.css"

export default function Formulario({ url, setUrl, maxComentarios, setMaxComentarios, onAnalizar, cargando, error }) {
  useEffect(() => {
    const slider = document.querySelector('input[type="range"]')
    if (slider) {
      const pct = ((maxComentarios - 1) / 9) * 100
      slider.style.setProperty('--pct', pct)
    }
  }, [maxComentarios])

  return (
    <div className="formulario glass section-gap fade-up fade-up-2">
      <label className="form-label">URL de la publicación</label>
      <div className="input-wrapper">
        <span className="input-icon">🔗</span>
        <input
          className="url-input"
          type="text"
          value={url}
          onChange={e => setUrl(e.target.value)}
          placeholder="https://www.facebook.com/..."
        />
      </div>

      <label className="form-label">Comentarios a analizar</label>
      <div className="slider-row">
        <div>
          <div className="slider-value">{maxComentarios}</div>
          <div className="slider-unit">comentarios</div>
        </div>
      </div>
      <input
        type="range"
        min={1} max={10} step={1}
        value={maxComentarios}
        onChange={e => setMaxComentarios(Number(e.target.value))}
      />
      <div className="slider-ticks">
        <span>1</span><span>3</span><span>5</span><span>7</span><span>10</span>
      </div>

      <button className="btn-analizar" onClick={onAnalizar} disabled={cargando}>
        {cargando
          ? <span className="btn-loading"><span className="spinner" /> Analizando comentarios...</span>
          : "Analizar comentarios →"
        }
      </button>

      {error && <div className="error-msg">⚠️ {error}</div>}
    </div>
  )
}