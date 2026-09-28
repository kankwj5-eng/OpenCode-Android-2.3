# OpenCode Android

Port experimental de OpenCode para Android, basado en **OpenCode 1.18.32**. La compilación de prueba documentada actualmente es **Android 2.3 (ARM64)**.

> **Estado: prueba experimental.** El port funciona en Android, pero todavía tiene limitaciones importantes propias del entorno actual.

## Estado actual

La aplicación inicia y permite utilizar la interfaz de OpenCode directamente desde Android. En las pruebas reales realizadas en el teléfono funcionan:

- Chat y sesiones.
- Visualización de archivos modificados y cambios realizados por el agente.
- Selector y búsqueda de modelos/proveedores.
- Modo de trabajo **Build**.
- Instalación de paquetes compatibles mediante `tool_install`.
- Descarga de archivos públicos mediante `browser_download`.
- Clonado de repositorios de GitHub mediante `repository_clone`.
- Desarrollo web con JavaScript/TypeScript, HTML5, CSS y WebGL/Three.js.
- Ejecución sobre Bun y las herramientas compatibles con el entorno actual.

Las capturas de prueba muestran al agente modificando un proyecto web directamente desde el teléfono y detectando los archivos modificados.

## Limitaciones actuales

OpenCode se ejecuta dentro de Android y el agente permanece limitado por el **entorno/sandbox que proporciona actualmente el port**. Los recursos disponibles para el agente —incluida la RAM utilizable y las capacidades de ejecución— dependen de ese entorno; todavía no equivalen a acceso nativo completo a toda la potencia del teléfono.

En esta versión, el trabajo práctico está centrado principalmente en tecnologías web y herramientas compatibles con **JavaScript/TypeScript/Bun**. El agente no dispone actualmente de un entorno Linux/desktop nativo completo para ejecutar libremente cualquier binario.

Aunque puede crear y modificar proyectos web, instalar paquetes compatibles, descargar archivos y clonar repositorios, **actualmente no debe considerarse capaz de ejecutar directamente motores y toolchains de escritorio como Godot ni de generar APK mediante un SDK Android/Gradle/JVM completo desde su sandbox actual**.

Estas limitaciones corresponden al estado actual del port y no representan el objetivo final.

## Próxima etapa: Termux como capa de ejecución

Está prevista la integración de **Termux como capa de ejecución inferior al entorno agéntico de OpenCode**.

La idea es mantener la interfaz y experiencia del agente de OpenCode mientras Termux proporciona un entorno Linux más completo en el propio teléfono. El objetivo es reducir las restricciones del sandbox y aprovechar mucho mejor los recursos disponibles del dispositivo.

Esta integración todavía **no está implementada** en Android 2.3 y se documenta como trabajo futuro.

## Navegador y automatización

Actualmente existen herramientas para descargar recursos y trabajar con Internet, pero se prevé incorporar un **navegador controlable directamente por el agente**, capaz de navegar páginas, buscar e interactuar con sitios como parte de tareas más completas.

También se prevé ampliar la integración con GitHub, el manejo de archivos, las herramientas disponibles y la automatización desde Android.

## APK

Compilación de prueba actual: `OpenCode_Android_2_3_Diagnostico_arm64.apk`

Arquitectura: **ARM64**.

## Instalación

1. Descarga el APK ARM64 de la versión correspondiente.
2. Permite la instalación desde esa fuente si Android lo solicita.
3. Instala y abre OpenCode.
4. Configura el proveedor/modelo que quieras utilizar.

## Seguridad

No publiques claves API, tokens de GitHub ni otras credenciales dentro del repositorio. Las credenciales deben configurarse localmente.

## Capturas y pruebas

Las capturas corresponden a pruebas reales realizadas en Android y documentan el selector de modelos, el chat, Build, las modificaciones de archivos y las limitaciones detectadas en el entorno actual.

## Código fuente

El objetivo es mantener aquí el código fuente del port y relacionar cada APK publicado con su versión correspondiente.

## Hoja de ruta

- Integración de Termux como backend/capa de ejecución.
- Mayor acceso a las capacidades y recursos del teléfono.
- Navegador controlable por el agente.
- Integración más completa con GitHub.
- Más herramientas y automatización.
- Ampliación progresiva más allá del desarrollo web.

La hoja de ruta describe objetivos previstos y **no implica que esas funciones estén disponibles actualmente**.

## Créditos

Proyecto experimental de port de OpenCode para Android. OpenCode y los nombres de proveedores, modelos y herramientas mencionados pertenecen a sus respectivos autores y propietarios.
