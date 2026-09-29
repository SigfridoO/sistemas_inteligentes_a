# Habilitar entornos virtuales de Python en Windows PowerShell

En Windows PowerShell, la activación de un entorno virtual de Python puede bloquearse debido a la política de ejecución de scripts.

Este documento muestra cómo habilitar la ejecución del script `Activate.ps1` de forma segura para el usuario actual.

## 1. Verificar la política de ejecución actual

Abre **PowerShell** y ejecuta:

```powershell
Get-ExecutionPolicy -List
```

Se mostrará una salida similar a:

```text
Scope          ExecutionPolicy
-----          ---------------
MachinePolicy  Undefined
UserPolicy     Undefined
Process        Undefined
CurrentUser    Undefined
LocalMachine   Restricted
```

## 2. Habilitar scripts para el usuario actual

La opción recomendada para un entorno de desarrollo es:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

PowerShell solicitará confirmación.

Por ejemplo:

```text
¿Desea cambiar la directiva de ejecución?
[S] Sí  [N] No
```

Selecciona:

```text
S
```

Esta configuración permite ejecutar scripts creados localmente y exige que los scripts descargados desde Internet estén firmados.

No es necesario utilizar `Unrestricted` ni modificar la política de `LocalMachine`.

## 3. Crear un entorno virtual

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
```

También puede utilizarse otro nombre, por ejemplo:

```powershell
python -m venv venv
```

## 4. Activar el entorno virtual

Si el entorno se llama `.venv`:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si el entorno se llama `venv`:

```powershell
.\venv\Scripts\Activate.ps1
```

Cuando el entorno se activa correctamente, PowerShell mostrará su nombre al inicio de la línea de comandos. Por ejemplo:

```text
(.venv) PS C:\ruta\del\proyecto>
```

## 5. Desactivar el entorno virtual

Para salir del entorno virtual:

```powershell
deactivate
```

## Opción temporal

Si no se desea modificar permanentemente la política de ejecución del usuario, puede habilitarse únicamente para la sesión actual de PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Después se activa normalmente el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

La configuración `Bypass` desaparecerá automáticamente al cerrar esa ventana de PowerShell.

## Configuración recomendada

Para un equipo utilizado regularmente para desarrollo con Python, se recomienda ejecutar una sola vez:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Posteriormente, para cada proyecto únicamente será necesario activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Resumen de comandos

```powershell
# Consultar políticas de ejecución
Get-ExecutionPolicy -List

# Habilitar scripts para el usuario actual
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Desactivar entorno virtual
deactivate
```