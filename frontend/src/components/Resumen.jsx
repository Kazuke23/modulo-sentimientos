import "../styles/Resumen.css"

export default function Resumen({ resumen, total }) {
  return (
    <div className="resumen-grid fade-up fade-up-3">
      <div className="resumen-card card-pos">
        <div className="card-icon">😊</div>
        <div className="card-numero">{resumen.POS}</div>
        <div className="card-label">Positivo</div>
      </div>
      <div className="resumen-card card-neg">
        <div className="card-icon">😠</div>
        <div className="card-numero">{resumen.NEG}</div>
        <div className="card-label">Negativo</div>
      </div>
      <div className="resumen-card card-neu">
        <div className="card-icon">😐</div>
        <div className="card-numero">{resumen.NEU}</div>
        <div className="card-label">Neutro</div>
      </div>
      <div className="resumen-card card-total">
        <div className="card-icon">📊</div>
        <div className="card-numero">{total}</div>
        <div className="card-label">Total</div>
      </div>
    </div>
  )
}