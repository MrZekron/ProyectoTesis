from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Dispositivo, TanqueAgua, Usuario
from .forms import DispositivoForm, TanqueAguaForm, UsuarioForm

# -------------------------
# REGISTRAR DISPOSITIVO
# -------------------------
def registrar_dispositivo(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dispositivo registrado correctamente.')
            return redirect('registrar_dispositivo')
        else:
            messages.error(request, 'Error al registrar el dispositivo. Por favor, corrige los errores.')
    else:
        form = DispositivoForm()

    return render(request, 'dispositivos/registro_dispositivo.html', {'form': form})

# -------------------------
# REGISTRAR TANQUE DE AGUA
# -------------------------
def registrar_tanque_agua(request):
    if request.method == 'POST':
        form = TanqueAguaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tanque de agua registrado correctamente.')
            return redirect('registrar_tanque_agua')
        else:
            messages.error(request, 'Error al registrar el tanque de agua. Por favor, corrige los errores.')
    else:
        form = TanqueAguaForm()

    return render(request, 'tanques/registro_tanque.html', {'form': form})

# -------------------------
# REGISTRAR USUARIO
# -------------------------
def registrar_usuario(request):
    # Si la petición es POST, significa que el formulario fue enviado
    if request.method == 'POST':
        form = UsuarioForm(request.POST)  # Creamos el formulario con los datos enviados
        if form.is_valid():
            usuario = form.save(commit=False)  # Guardamos los datos, pero aún no en la DB
            usuario.set_password(form.cleaned_data['contrasena'])  # Encriptamos la contraseña
            usuario.save()  # Ahora sí lo guardamos en la DB
            messages.success(request, 'Usuario registrado exitosamente 🎉')
            request.session['usuario_id'] = usuario.id  # Inicia sesión automáticamente
            return redirect('menu')  # Redirige a menu.html
        else:
            messages.error(request, 'Revisa los datos, algo no está bien 😥')
    else:
        form = UsuarioForm()  # Si no es POST, mostramos el formulario vacío

    return render(request, 'usuarios/registro_usuario.html', {'form': form})




# -------------------------
# INICIAR SESIÓN
# -------------------------
def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('correo')  # Obtenemos el email desde el formulario
        contrasena = request.POST.get('contrasena')  # Obtenemos la contraseña

        try:
            # Buscamos si existe un usuario con ese email
            usuario = Usuario.objects.get(email=email)
            # Verificamos si la contraseña coincide usando el método del modelo
            if usuario.check_password(contrasena):
                request.session['usuario_id'] = usuario.id  # Guardamos el ID en sesión
                messages.success(request, f'¡Bienvenido {usuario.nombre}! 👋')
                return redirect('menu')  # Redirigimos a la vista "menu"
            else:
                messages.error(request, 'Contraseña incorrecta 😕')  # Mensaje si la contraseña no coincide
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo ingresado no está registrado ❌')  # Mensaje si no hay usuario

    return render(request, 'usuarios/iniciar_sesion.html')  # Mostramos el template

# -------------------------
# MENU
# -------------------------

def menu(request):
    tanques = TanqueAgua.objects.all()
    return render(request, 'usuarios/menu.html', {'tanques': tanques})



# -------------------------
# VISTA DE INICIO
# -------------------------
def inicio(request):
    return render(request, 'index.html')
