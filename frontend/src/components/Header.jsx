import "../styles/Header.css"

export default function Header() {
  return (
    <header className="header fade-up fade-up-1">
      <div className="header-badge">
        <span className="dot" />
        Análisis en tiempo real
      </div>
      <h1>Sentiment<br />Intelligence</h1>
      <p>Descubre el sentimiento detrás de cada comentario en Facebook con inteligencia artificial en español</p>
    </header>
  )
}