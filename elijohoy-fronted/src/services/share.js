import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

/**
 * Servicio para compartir y descargar resultados del test
 */
const shareService = {
  /**
   * Generar HTML del certificado de resultados
   * @param {Object} perfil - Objeto con los datos del perfil
   * @param {string} avatarUrl - URL de la imagen del avatar
   * @returns {string} HTML del certificado
   */
  generarHTMLCertificado(perfil, avatarUrl = '') {
    const coloresMap = {
      'INTJ': '#6366F1',
      'INTP': '#3B82F6',
      'ENTJ': '#EF4444',
      'ENTP': '#F97316',
      'INFJ': '#EC4899',
      'INFP': '#10B981',
      'ENFJ': '#FBBF24',
      'ENFP': '#06B6D4',
      'ISTJ': '#92400E',
      'ISFJ': '#0D9488',
      'ESTJ': '#B45309',
      'ESFJ': '#84CC16',
      'ISTP': '#4F46E5',
      'ISFP': '#22D3EE',
      'ESTP': '#F59E0B',
      'ESFP': '#3B82F6'
    }

    const colorPrincipal = coloresMap[perfil.tipo.codigo] || '#6366F1'

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f3f4f6; }
          .container { width: 100%; max-width: 800px; margin: 0 auto; background: white; padding: 10px; }
          .header { text-align: center; margin-bottom: 6px; background: linear-gradient(135deg, ${colorPrincipal} 0%, ${colorPrincipal}dd 100%); color: white; padding: 8px 6px; border-radius: 8px; }
          .avatar-container { text-align: center; margin-bottom: 4px; }
          .avatar-image { max-width: 120px; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); }
          .header h1 { font-size: 20px; font-weight: bold; margin-bottom: 1px; }
          .header .codigo { font-size: 16px; opacity: 0.9; }
          .header .nombre { font-size: 13px; margin-top: 2px; opacity: 0.95; }
          .section { margin-bottom: 6px; }
          .section-title { font-size: 12px; font-weight: bold; color: ${colorPrincipal}; margin-bottom: 3px; border-bottom: 1px solid ${colorPrincipal}; padding-bottom: 2px; }
          .descripcion { font-size: 10px; line-height: 1.3; color: #374151; margin-bottom: 4px; }
          .dimensiones { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; }
          .dimension-box { padding: 4px; background: #f9fafb; border-left: 2px solid ${colorPrincipal}; border-radius: 3px; }
          .dimension-label { font-weight: bold; color: #1f2937; font-size: 9px; }
          .dimension-score { font-size: 14px; font-weight: bold; color: ${colorPrincipal}; margin-top: 1px; }
          .contenido { color: #4b5563; font-size: 9px; line-height: 1.3; }
          .footer { text-align: center; margin-top: 6px; padding-top: 4px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 8px; }
          .porcentaje { text-align: center; padding: 5px; background: #f0f9ff; border-radius: 4px; margin-top: 6px; }
          .porcentaje-numero { font-size: 20px; font-weight: bold; color: ${colorPrincipal}; }
          .porcentaje-texto { font-size: 9px; color: #6b7280; margin-top: 1px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="avatar-container">
            ${avatarUrl ? `<img src="${avatarUrl}" alt="${perfil.tipo.codigo}" class="avatar-image" />` : ''}
          </div>
          
          <div class="header">
            <h1>${perfil.tipo.codigo}</h1>
            <div class="codigo">Tipo de Personalidad</div>
            <div class="nombre">${perfil.tipo.nombre}</div>
          </div>

          <div class="section">
            <div class="section-title">Descripción</div>
            <div class="descripcion">${perfil.tipo.descripcion_completa.substring(0, 120)}</div>
          </div>

          <div class="section">
            <div class="section-title">Tus Dimensiones</div>
            <div class="dimensiones">
              <div class="dimension-box">
                <div class="dimension-label">${perfil.dimensiones.extraversion_introversion}</div>
                <div class="dimension-score">${perfil.puntuaciones.IE}</div>
              </div>
              <div class="dimension-box">
                <div class="dimension-label">${perfil.dimensiones.intuicion_sensacion}</div>
                <div class="dimension-score">${perfil.puntuaciones.SN}</div>
              </div>
              <div class="dimension-box">
                <div class="dimension-label">${perfil.dimensiones.pensamiento_sentimiento}</div>
                <div class="dimension-score">${perfil.puntuaciones.FT}</div>
              </div>
              <div class="dimension-box">
                <div class="dimension-label">${perfil.dimensiones.percepcion_juicio}</div>
                <div class="dimension-score">${perfil.puntuaciones.JP}</div>
              </div>
            </div>
          </div>

          <div class="section">
            <div class="section-title">Fortalezas</div>
            <div class="contenido">${perfil.tipo.fortalezas.substring(0, 100)}</div>
          </div>

          <div class="section">
            <div class="section-title">Áreas de Mejora</div>
            <div class="contenido">${perfil.tipo.debilidades.substring(0, 100)}</div>
          </div>

          <div class="section">
            <div class="section-title">Carreras Sugeridas</div>
            <div class="contenido">${perfil.tipo.carreras_sugeridas.substring(0, 100)}</div>
          </div>

          <div class="porcentaje">
            <div class="porcentaje-numero">${perfil.tipo.porcentaje_poblacion}%</div>
            <div class="porcentaje-texto">de la población tiene tu tipo</div>
          </div>

          <div class="footer">
            <p>ElijoHoy - Test de Personalidad</p>
          </div>
        </div>
      </body>
      </html>
    `
  },

  /**
   * Descargar resultados como PDF
   * @param {Object} perfil - Objeto con los datos del perfil
   * @param {string} avatarUrl - URL de la imagen del avatar
   */
  async descargarPDF(perfil, avatarUrl = '') {
    try {
      const html = this.generarHTMLCertificado(perfil, avatarUrl)
      const div = document.createElement('div')
      div.innerHTML = html
      div.style.position = 'absolute'
      div.style.left = '-9999px'
      document.body.appendChild(div)

      const canvas = await html2canvas(div.querySelector('.container'), {
        scale: 1.2,
        useCORS: true,
        allowTaint: true,
        logging: false,
        backgroundColor: '#ffffff'
      })

      document.body.removeChild(div)

      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      })

      const imgWidth = 210 // A4 width in mm
      const pageHeight = 297 // A4 height in mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      let heightLeft = imgHeight

      let position = 0

      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pageHeight

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight
        pdf.addPage()
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
        heightLeft -= pageHeight
      }

      const nombreArchivo = `Resultado_${perfil.tipo.codigo}_${new Date().getTime()}.pdf`
      pdf.save(nombreArchivo)
      
      return { success: true, message: 'PDF descargado exitosamente' }
    } catch (error) {
      console.error('Error al descargar PDF:', error)
      return { success: false, message: 'Error al descargar PDF' }
    }
  },

  /**
   * Descargar resultados como imagen
   * @param {Object} perfil - Objeto con los datos del perfil
   * @param {string} avatarUrl - URL de la imagen del avatar
   */
  async descargarImagen(perfil, avatarUrl = '') {
    try {
      const html = this.generarHTMLCertificado(perfil, avatarUrl)
      const div = document.createElement('div')
      div.innerHTML = html
      div.style.position = 'absolute'
      div.style.left = '-9999px'
      document.body.appendChild(div)

      const canvas = await html2canvas(div.querySelector('.container'), {
        scale: 1.5,
        useCORS: true,
        allowTaint: true,
        logging: false,
        backgroundColor: '#ffffff'
      })

      document.body.removeChild(div)

      const link = document.createElement('a')
      link.href = canvas.toDataURL('image/png')
      link.download = `Resultado_${perfil.tipo.codigo}_${new Date().getTime()}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      return { success: true, message: 'Imagen descargada exitosamente' }
    } catch (error) {
      console.error('Error al descargar imagen:', error)
      return { success: false, message: 'Error al descargar imagen' }
    }
  },

  /**
   * Generar imagen para compartir en redes sociales
   * @param {Object} perfil - Objeto con los datos del perfil
   * @param {string} avatarUrl - URL de la imagen del avatar
   * @returns {Promise<string>} Data URL de la imagen
   */
  async generarImagenCompartible(perfil, avatarUrl = '') {
    try {
      const html = this.generarHTMLCertificado(perfil, avatarUrl)
      const div = document.createElement('div')
      div.innerHTML = html
      div.style.position = 'absolute'
      div.style.left = '-9999px'
      document.body.appendChild(div)

      const canvas = await html2canvas(div.querySelector('.container'), {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        logging: false,
        backgroundColor: '#ffffff'
      })

      document.body.removeChild(div)
      return canvas.toDataURL('image/png')
    } catch (error) {
      console.error('Error al generar imagen para compartir:', error)
      throw error
    }
  },

  /**
   * Compartir en WhatsApp
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async compartirWhatsApp(perfil) {
    try {
      const texto = `¡Descubrí mi tipo de personalidad en ElijoHoy! 🎯\n\n${perfil.tipo.codigo}\n${perfil.tipo.nombre}\n\n¿Quieres saber cuál es el tuyo? https://elijohoy.com`
      const textoEncoded = encodeURIComponent(texto)
      
      window.open(`https://wa.me/?text=${textoEncoded}`, '_blank')
    } catch (error) {
      console.error('Error compartiendo en WhatsApp:', error)
      const texto = encodeURIComponent(`¡Descubrí mi tipo de personalidad: ${perfil.tipo.codigo} en ElijoHoy! 🎯`)
      window.open(`https://wa.me/?text=${texto}`, '_blank')
    }
  },

  /**
   * Compartir en Instagram con imagen
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async compartirInstagram(perfil) {
    try {
      const mensaje = `¡Descubrí mi tipo de personalidad en ElijoHoy! 🎯 ${perfil.tipo.codigo} - ${perfil.tipo.nombre} ¿Y tú cuál eres? #ElijoHoy #PersonalidadTest #MBTITest`
      await navigator.clipboard.writeText(mensaje)
      alert(`Mensaje copiado: ${mensaje}\n\nAbre Instagram y comparte esta imagen en tu historia`)
    } catch (error) {
      console.error('Error compartiendo en Instagram:', error)
      alert('Abre Instagram y comparte tu resultado')
    }
  },

  /**
   * Compartir en Facebook
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async compartirFacebook(perfil) {
    try {
      const url = encodeURIComponent('https://elijohoy.com')
      const quote = encodeURIComponent(
        `¡Descubrí mi tipo de personalidad: ${perfil.tipo.codigo} - ${perfil.tipo.nombre} en ElijoHoy! 🎯`
      )
      window.open(
        `https://www.facebook.com/sharer/sharer.php?u=${url}&quote=${quote}`,
        '_blank'
      )
    } catch (error) {
      console.error('Error compartiendo en Facebook:', error)
    }
  },

  /**
   * Compartir en Messenger
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async compartirMessenger(perfil) {
    try {
      alert(`¡Comparte tu tipo: ${perfil.tipo.codigo} - ${perfil.tipo.nombre} en Messenger!`)
    } catch (error) {
      console.error('Error compartiendo en Messenger:', error)
    }
  },

  /**
   * Compartir en Twitter/X
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async compartirTwitter(perfil) {
    try {
      const texto = encodeURIComponent(
        `¡Descubrí mi tipo de personalidad: ${perfil.tipo.codigo} - ${perfil.tipo.nombre} en ElijoHoy! 🎯 ` +
        `Descubre el tuyo en https://elijohoy.com #ElijoHoy #PersonalidadTest #MBTI`
      )
      window.open(`https://twitter.com/intent/tweet?text=${texto}`, '_blank')
    } catch (error) {
      console.error('Error compartiendo en Twitter:', error)
    }
  },

  /**
   * Compartir en LinkedIn
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async compartirLinkedIn(perfil) {
    try {
      // Usa perfil para obtener el tipo de personalidad para futuras mejoras
      const url = encodeURIComponent('https://elijohoy.com?tipo=' + perfil.tipo.codigo)
      window.open(
        `https://www.linkedin.com/sharing/share-offsite/?url=${url}`,
        '_blank'
      )
    } catch (error) {
      console.error('Error compartiendo en LinkedIn:', error)
    }
  },

  /**
   * Compartir por correo electrónico
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async compartirEmail(perfil) {
    try {
      const subject = encodeURIComponent('¡Descubrí mi tipo de personalidad en ElijoHoy!')
      const body = encodeURIComponent(
        `Hola!\n\n` +
        `Acabo de descubrir que mi tipo de personalidad es:\n\n` +
        `Tipo: ${perfil.tipo.codigo}\n` +
        `Nombre: ${perfil.tipo.nombre}\n\n` +
        `Descripción: ${perfil.tipo.descripcion_completa.substring(0, 100)}...\n\n` +
        `Mis Dimensiones:\n` +
        `• ${perfil.dimensiones.extraversion_introversion}: ${perfil.puntuaciones.IE}\n` +
        `• ${perfil.dimensiones.intuicion_sensacion}: ${perfil.puntuaciones.SN}\n` +
        `• ${perfil.dimensiones.pensamiento_sentimiento}: ${perfil.puntuaciones.FT}\n` +
        `• ${perfil.dimensiones.percepcion_juicio}: ${perfil.puntuaciones.JP}\n\n` +
        `¿Quieres saber cuál es tu tipo de personalidad? ¡Realiza el test aquí!\n` +
        `https://elijohoy.com`
      )
      window.open(`mailto:?subject=${subject}&body=${body}`, '_blank')
    } catch (error) {
      console.error('Error preparando email:', error)
    }
  },

  /**
   * Copiar al portapapeles un resumen de los resultados
   * @param {Object} perfil - Objeto con los datos del perfil
   */
  async copiarAlPortapapeles(perfil) {
    try {
      const resumen = `
Mi Tipo de Personalidad: ${perfil.tipo.código} - ${perfil.tipo.nombre}

Mis Dimensiones:
• ${perfil.dimensiones.extraversion_introversion}: ${perfil.puntuaciones.IE}
• ${perfil.dimensiones.intuicion_sensacion}: ${perfil.puntuaciones.SN}
• ${perfil.dimensiones.pensamiento_sentimiento}: ${perfil.puntuaciones.FT}
• ${perfil.dimensiones.percepcion_juicio}: ${perfil.puntuaciones.JP}

${perfil.tipo.descripcion_corta}

Descubre tu tipo de personalidad en: https://elijohoy.com
      `.trim()

      await navigator.clipboard.writeText(resumen)
      return { success: true, message: 'Resultado copiado al portapapeles' }
    } catch (error) {
      console.error('Error al copiar al portapapeles:', error)
      return { success: false, message: 'Error al copiar al portapapeles' }
    }
  }
}

export default shareService
