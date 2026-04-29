import { useState } from "react"
import axios from "axios"
import "./styles/App.css"
import Header from "./components/Header"
import Formulario from "./components/Formulario"
import Resumen from "./components/Resumen"
import GraficaTorta from "./components/GraficaTorta"
import ListaComentarios from "./components/ListaComentarios"

export default function App() {
  const [url, setUrl] = useState("")
  const [maxComentarios, setMaxComentarios] = useState(10)
  const [resultado, setResultado] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState("")

  const analizar = async () => {
    if (!url) { setError("Por favor ingresa una URL de Facebook"); return }
    setCargando(true)
    setError("")
    setResultado(null)
    try {
      const res = await axios.post("https://icy-overfill-footpad.ngrok-free.dev/analizar", {
        url,
        max_comentarios: maxComentarios,
        },{
        headers: {
          "ngrok-skip-browser-warning": "true"
        }
      })
      setResultado(res.data)
    } catch {
      setError("Error al conectar con el servidor. ¿Está corriendo FastAPI?")
    } finally {
      setCargando(false)
    } 
  }

  return (
    <div className="app-wrapper">
      <Header />
      <Formulario
        url={url} setUrl={setUrl}
        maxComentarios={maxComentarios} setMaxComentarios={setMaxComentarios}
        onAnalizar={analizar} cargando={cargando} error={error}
      />
      {resultado && (
        <>
          <Resumen resumen={resultado.resumen} total={resultado.total_comentarios} />
          <GraficaTorta resumen={resultado.resumen} />
          <ListaComentarios comentarios={resultado.comentarios} />
        </>
      )}
    </div>
  )
}