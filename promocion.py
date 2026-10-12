import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Configuración de página con diseño ancho
st.set_page_config(page_title="Calculadora de Pérdida Operativa | IA & Ops", page_icon="⚡", layout="wide")

# Estilos CSS tipo SaaS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #f3f4f6; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Cabecera de alto impacto
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Calculá tu pérdida operativa en 1 minuto ⏱️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Descubrí cuántas horas y plata pierde tu negocio por mes en tareas manuales y repetitivas.</p>", unsafe_allow_html=True)
st.markdown("---")

col_input, col_dashboard = st.columns([1, 1.5], gap="large")

with col_input:
    st.subheader("⚙️ Parámetros de la Empresa")
    nombre_empresa = st.text_input("Nombre de la PyME / Negocio:", value="Empresa Modelo S.A.")
    empleados = st.number_input("Cantidad de empleados administrativos:", min_value=1, max_value=500, value=6)
    costo_hora_promedio = st.number_input("Costo estimado por hora ($ ARS):", min_value=1, value=6000)

    st.markdown("#### ⏱️ Tiempos en Tareas Mecánicas")
    atencion_cliente = st.slider("💬 FAQs y soporte repetitivo (hs/semana por pers.):", 0, 20, 6)
    carga_datos = st.slider("📋 Copia manual entre planillas (hs/semana por pers.):", 0, 20, 8)
    reportes_manuales = st.slider("📊 Armado de reportes (hs/semana por pers.):", 0, 20, 4)
    seguimiento_comercial = st.slider("🔄 Seguimiento comercial (hs/semana por pers.):", 0, 20, 5)

    st.markdown("#### 🎯 Situación Específica")
    otro_problema = st.text_area(
        "¿Tenés algún otro cuello de botella operativo específico?",
        placeholder="Ej: Pasamos pedidos de WhatsApp a Excel a mano..."
    )

# Cálculos
total_horas_semanales_persona = atencion_cliente + carga_datos + reportes_manuales + seguimiento_comercial
total_horas_mes_empresa = total_horas_semanales_persona * empleados * 4
costo_mensual_perdido = total_horas_mes_empresa * costo_hora_promedio

with col_dashboard:
    st.subheader("📊 Métricas de Fricción Operativa")
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Horas Perdidas / Mes", value=f"{total_horas_mes_empresa} hs")
    with kpi2:
        st.metric(label="Costo Mensual Oculto", value=f"$ {costo_mensual_perdido:,.0f}")
    with kpi3:
        st.metric(label="Potencial Automatizable", value="85%")

    st.markdown("---")
    
    # Gráfico con Plotly y etiquetas horizontales en el eje X
    st.markdown("#### 🔍 Desglose del Tiempo por Proceso (Horas / Semana por Empleado)")
    df_chart = pd.DataFrame({
        'Proceso': ['Atención y Soporte', 'Carga de Datos', 'Reportes Manuales', 'Seguimiento Comercial'],
        'Horas Semanales': [atencion_cliente, carga_datos, reportes_manuales, seguimiento_comercial]
    })

    fig = px.bar(
        df_chart, 
        x='Proceso', 
        y='Horas Semanales',
        text='Horas Semanales',
        color='Proceso',
        color_discrete_sequence=px.colors.sequential.Sunset
    )

    fig.update_layout(
        plot_bgcolor="#161b22",
        paper_bgcolor="#0e1117",
        font_color="#f3f4f6",
        xaxis=dict(tickangle=0), 
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Sección inferior de formulario
st.subheader("🚀 Generar Reporte Ejecutivo para Directivos")
with st.form(key="report_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        contacto_nombre = st.text_input("Nombre del Responsable:")
    with c2:
        email_contacto = st.text_input("Correo electrónico corporativo:")
    with c3:
        whatsapp_contacto = st.text_input("WhatsApp:")
        
    enviar_reporte = st.form_submit_button(label="📥 Enviar Diagnóstico y Propuesta Técnica")

    if enviar_reporte:
        if email_contacto and nombre_empresa:
            payload = {
                "empresa": nombre_empresa,
                "nombre": contacto_nombre,
                "email": email_contacto,
                "whatsapp": whatsapp_contacto,
                "empleados": empleados,
                "costo_hora": costo_hora_promedio,
                "horas_mes": total_horas_mes_empresa,
                "costo_perdido": costo_mensual_perdido,
                "problema_especifico": otro_problema
            }
            
            WEBHOOK_URL = "https://hook.us2.make.com/dp94bg6uesu8b5nd94s3nenh9j09q9hy"
            
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("¡Enviado a Make con éxito!")
                else:
                    st.warning(f"Error HTTP: {response.status_code}")
            except Exception as e:
                st.error(f"Fallo la conexión: {e}")
        else:
            st.error("Completá los campos obligatorios.")
            