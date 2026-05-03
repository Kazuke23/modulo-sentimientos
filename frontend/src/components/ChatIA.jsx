import { useState, useRef, useEffect } from "react"
import "../styles/ChatIA.css"

const SUGERENCIAS = [
  "¿Cuál es la opinión general sobre esta publicación?",
  "¿Quiénes están en contra y cuáles son sus argumentos?",
  "¿Qué temas se mencionan más en los comentarios?",
  "Resume los comentarios positivos",
  "¿Hay algún patrón o tendencia en los comentarios?",
]

export default function ChatIA({ comentarios, url }) {
  const [mensajes, setMensajes] = useState([
    {
      role: "assistant",
      content: `¡Hola! Analicé ${comentarios.length} comentarios de esta publicación. Puedes preguntarme cualquier cosa sobre ellos — opiniones, argumentos, tendencias, lo que necesites.`
    }
  ])
  const [input, setInput] = useState("")
  const [cargando, setCargando] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [mensajes])

  const contexto = `Eres un asistente experto en análisis de redes sociales y opinión pública.
Tienes acceso a ${comentarios.length} comentarios extraídos de esta publicación: ${url}

COMENTARIOS EXTRAÍDOS:
${comentarios.map((c, i) => `[${i+1}] Sentimiento: ${c.sentimiento} | Likes: ${c.likes}
Texto: ${c.texto_original || c.texto_limpio}`).join("\n\n")}

Instrucciones:
- Responde SIEMPRE en español
- Basa tus respuestas ÚNICAMENTE en los comentarios proporcionados
- Sé claro, conciso y útil
- Si te preguntan por argumentos específicos, cita fragmentos de los comentarios
- Si te preguntan quién está en contra o a favor, agrupa y explica sus razones`

  const enviar = async (pregunta) => {
    const texto = pregunta || input.trim()
    if (!texto || cargando) return

    const nuevosMs = [...mensajes, { role: "user", content: texto }]
    setMensajes(nuevosMs)
    setInput("")
    setCargando(true)

    try {
      const res = await fetch("https://modulo-sentimientos.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contexto: contexto,
          mensajes: nuevosMs.map(m => ({ role: m.role, content: m.content }))
        })
      })

      const data = await res.json()
      const respuesta = data.respuesta || "No pude generar una respuesta."
      setMensajes(prev => [...prev, { role: "assistant", content: respuesta }])
    } catch (e) {
      setMensajes(prev => [...prev, {
        role: "assistant",
        content: "Error al conectar con la IA. Intenta de nuevo."
      }])
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="chat-wrapper glass fade-up fade-up-4">
      <div className="section-title">Chat con IA — Analiza esta publicación</div>

      <div className="chat-sugerencias">
        {SUGERENCIAS.map((s, i) => (
          <button key={i} className="chip" onClick={() => enviar(s)} disabled={cargando}>
            {s}
          </button>
        ))}
      </div>

      <div className="chat-mensajes">
        {mensajes.map((m, i) => (
          <div key={i} className={`chat-burbuja ${m.role}`}>
            {m.content}
          </div>
        ))}
        {cargando && (
          <div className="chat-burbuja thinking">
            Analizando comentarios...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <input
          className="chat-input"
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && enviar()}
          placeholder="Pregunta algo sobre los comentarios..."
          disabled={cargando}
        />
        <button className="chat-btn" onClick={() => enviar()} disabled={cargando}>
          {cargando ? "..." : "Enviar →"}
        </button>
      </div>
    </div>
  )
}