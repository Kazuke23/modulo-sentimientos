import { useState } from "react"
import "../styles/ListaComentarios.css"

const ETIQUETAS = { POS: "Positivo", NEG: "Negativo", NEU: "Neutro" }
const ICONOS    = { POS: "↑", NEG: "↓", NEU: "—" }

export default function ListaComentarios({ comentarios }) {
  const [abierto, setAbierto] = useState(false)

  return (
    <div className="lista-wrapper glass fade-up fade-up-4">
      <button className="lista-toggle" onClick={() => setAbierto(!abierto)}>
        <div className="section-title" style={{ marginBottom: 0 }}>
          Comentarios extraídos ({comentarios.length})
        </div>
        <span className="lista-flecha">{abierto ? "▲" : "▼"}</span>
      </button>

      {abierto && (
        <div className="lista-contenido">
          {comentarios.map((c, i) => (
            <div key={i} className={`comentario-item ${c.sentimiento.toLowerCase()}`}>
              <div className="comentario-top">
                <span className={`badge badge-${c.sentimiento.toLowerCase()}`}>
                  {ICONOS[c.sentimiento]} {ETIQUETAS[c.sentimiento]}
                </span>
                <div className="comentario-meta">
                  <span>👍 {c.likes}</span>
                  <span>{new Date(c.fecha).toLocaleDateString("es-CO", { day:"numeric", month:"short", year:"numeric" })}</span>
                </div>
              </div>
              <p className="comentario-texto">{c.texto_limpio}</p>
              <div className="probas-bar">
                {[["pos","POS","positivo"],["neg","NEG","negativo"],["neu","NEU","neutro"]].map(([cls, key, label]) => (
                  <div key={key} className="proba-item">
                    <div className={`proba-label ${cls}`}>{label}</div>
                    <div className="proba-value">{c.probabilidades[label === "positivo" ? "positivo" : label === "negativo" ? "negativo" : "neutro"]}</div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}