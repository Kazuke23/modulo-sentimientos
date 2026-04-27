import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts"
import "../styles/GraficaTorta.css"

const COLORES  = { POS: "#10B981", NEG: "#EF4444", NEU: "#F59E0B" }
const ETIQUETAS = { POS: "Positivo", NEG: "Negativo", NEU: "Neutro" }

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    const { name, value } = payload[0]
    return (
      <div style={{ background:"rgba(8,11,20,0.95)", border:"1px solid rgba(255,255,255,0.1)", borderRadius:10, padding:"10px 16px" }}>
        <div style={{ fontFamily:"var(--font-display)", fontSize:13, fontWeight:700, color:"#F0F4FF", marginBottom:2 }}>{name}</div>
        <div style={{ fontSize:22, fontWeight:800, color: payload[0].payload.fill }}>{value}</div>
      </div>
    )
  }
  return null
}

export default function GraficaTorta({ resumen }) {
  const data = Object.entries(resumen).map(([key, value]) => ({
    name: ETIQUETAS[key], value, key, fill: COLORES[key]
  }))

  return (
    <div className="grafica-wrapper glass section-gap fade-up fade-up-3">
      <div className="section-title">Distribución de sentimientos</div>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%" cy="50%"
            innerRadius={70}
            outerRadius={110}
            paddingAngle={4}
            label={({ name, percent }) => percent > 0 ? `${(percent*100).toFixed(0)}%` : ""}
            labelLine={false}
          >
            {data.map(entry => (
              <Cell
                key={entry.key}
                fill={entry.fill}
                stroke="transparent"
                style={{ filter: `drop-shadow(0 0 8px ${entry.fill}60)` }}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            formatter={(value) => <span style={{ color:"#7A8BA0", fontSize:13 }}>{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}