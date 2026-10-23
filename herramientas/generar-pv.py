#!/usr/bin/env python3
"""Genera las hojas ING-PV-02 a 09 (una partícula por hoja) a partir de los datos de abajo.
Uso: python3 herramientas/generar-pv.py hojas/ing-pv
Después: node herramientas/construir.mjs hojas/ing-pv/*.html
Convenciones: en la forma, "_" = hueco del objeto; en la pronunciación, *X* = sílaba fuerte.
Las hojas ING-PV-01, E1 y E2 se escriben a mano."""
import re, sys

DESTINO = sys.argv[1]
FECHA = '2026-10-17'

def forma(s):
    return re.sub(r'_', '<i class="obj"></i>', s)

def pron(s):
    return re.sub(r'\*(.+?)\*', r'<span class="tonica">\1</span>', s)

def verbo(v):
    pv, pr, sig, ej, tr, *resto = v
    marca = f' <span class="marca">{resto[0]}</span>' if resto and resto[0] else ''
    return (f'        <div class="verbo"><span class="pv">{forma(pv)}</span><span class="pron">{pron(pr)}</span> '
            f'<span class="sig">{sig}</span>{marca}<span class="ej">{ej}</span><span class="tr">{tr}</span></div>')

def rama(i, r):
    titulo, glosa, verbos = r
    lit = ' literal' if i == 1 else ''
    num = 'num azul' if i == 1 else 'num'
    filas = '\n'.join(verbo(v) for v in verbos)
    return (f'      <div class="rama{lit}">\n'
            f'        <div class="cab"><span class="{num}">{i}</span><span class="t">{titulo}</span><span class="g">{glosa}</span></div>\n'
            f'{filas}\n      </div>')

def hoja(h):
    r = h['ramas']
    items = '\n'.join(
        f'        <div class="item"><span class="letra">{l}</span><span>{t}</span></div>'
        for l, t in zip('abcd', h['practica']))
    notas = '\n'.join(h['notas'])
    pareja = h.get('pareja', '')
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{h['codigo']} {h['titulo']}</title>
<link rel="stylesheet" href="../../estilo/combi.css">
<link rel="stylesheet" href="../../estilo/llegada.css">
<link rel="stylesheet" href="../../estilo/escritura.css">
<link rel="stylesheet" href="../../estilo/phrasal.css">
</head>
<body>
<div class="hoja">
  <header class="cabecera">
    <div class="codigo">{h['codigo']}</div>
    <div>
      <span class="coleccion">Phrasal verbs por partícula · {h['n']} de 9</span>
      <h1 class="titulo">{h['titulo']}</h1>
      <p class="bajada">{h['bajada']}</p>
    </div>
    <div class="lateral">{h['lateral']}<br>Cómo leer la hoja: ING-PV-01</div>
  </header>

  <main class="cuerpo">
    <div class="radial" data-hero>
{rama(1, r[0])}

{rama(2, r[1])}

      <div class="centro">
        <div class="literal">
          <svg class="esquema" data-particula="{h['particula']}"></svg>
          <p><b>Sentido literal</b>{h['literal']}</p>
        </div>
        <div class="nucleo"><span class="p{' largo' if len(h['particula']) > 3 else ''}">{h['particula'].upper()}</span><span class="pron">{pron(h['pron'])}</span></div>
        <div class="idea">{h['idea']}<span class="refs"><span class="ref">{h['murphy']}</span></span></div>
      </div>

{rama(3, r[2])}

{rama(4, r[3])}
    </div>
    <p class="leyenda-pv"><i class="obj"></i> = el objeto; si es pronombre, va ahí: <span class="en">{h['ley_bien']}</span>, no <span class="mal">{h['ley_mal']}</span>. Sin hueco: sin objeto. MAYÚSCULA: sílaba fuerte.</p>
{pareja}
    <div class="banda">
      <div class="practica">
        <div class="seccion"><span class="num">✎</span><span class="h2">Practicá</span></div>
{items}
        <p class="soluciones">{h['soluciones']}</p>
      </div>
      <div class="notas">
{notas}
      </div>
    </div>
  </main>

  <footer class="pie">
    <span>{h['codigo']} · versión 1 · {FECHA}</span>
    <span class="fuentes">{h['fuentes']} Grupos: modelo cognitivo, ver ING-PV-01. Consultado el {FECHA}.</span>
    <span>Enciclopedia para imprimir</span>
  </footer>
</div>
<script src="../../estilo/particulas.js"></script>
<script src="../../estilo/radial.js"></script>
</body>
</html>
'''

H = '<span class="hueco"></span>'
C = '<span class="hueco corto"></span>'

def kiwi(titulo, pares):
    filas = '\n'.join(f'            <dt>{a}</dt><dd>{b}</dd>' for a, b in pares)
    return (f'        <div class="kiwi">\n          <span class="h3">{titulo}</span>\n          <dl>\n{filas}\n          </dl>\n        </div>')

def alerta(t, p):
    return f'        <div class="alerta"><b>{t}</b><p>{p}</p></div>'

SUST = 'Como sustantivo, el acento va adelante'

HOJAS = [
 dict(codigo='ING-PV-02', n=2, particula='up', pron='ap', titulo='UP: hacia arriba',
  bajada='Y de ahí: lo que aumenta, lo que se completa, lo que aparece y lo que se despierta.',
  lateral='Su opuesto: DOWN, ING-PV-03', literal='De abajo hacia arriba, hasta el tope.',
  idea='Lo que sube es <b>más</b>; lo que llega al tope está <b>completo</b>; lo que se levanta <b>se ve</b>; quien se levanta está <b>despierto</b>.',
  murphy='Murphy U142–144', ley_bien='pick it up', ley_mal='pick up it',
  ramas=[
   ('Hacia arriba', 'el sentido literal', [
     ('get up', 'guet *AP*', 'levantarse (de la cama)', 'I get up at six on work days.', 'Me levanto a las seis los días de trabajo.'),
     ('pick _ up', 'pik *AP*', 'levantar; pasar a buscar', 'Can you pick me up at the hostel?', '¿Me pasás a buscar por el hostel?'),
     ('set _ up', 'set *AP*', 'armar, instalar; abrir (una cuenta)', 'We set up the tables before opening.', 'Armamos las mesas antes de abrir.')]),
   ('Más', 'arriba = más cantidad', [
     ('turn _ up', 'tern *AP*', 'subir (volumen, calefacción)', 'Can you turn the heater up?', '¿Podés subir la estufa?'),
     ('go up', 'gou *AP*', 'subir, aumentar (precios)', 'The rent is going up in March.', 'El alquiler aumenta en marzo.'),
     ('speed up', 'spiid *AP*', 'acelerar, apurarse', 'We need to speed up: the truck arrives at ten.', 'Hay que apurarse: el camión llega a las diez.')]),
   ('Hasta el final', 'arriba = completo', [
     ('use _ up', 'iuuz *AP*', 'gastar todo', 'Who used up all the milk?', '¿Quién se terminó toda la leche?'),
     ('clean _ up', 'kliin *AP*', 'limpiar y ordenar todo', 'Can you clean up this mess?', '¿Podés limpiar este desorden?'),
     ('wash up', 'uosh *AP*', 'lavar los platos', "I'll wash up tonight: you cooked.", 'Esta noche lavo yo: vos cocinaste.', 'NZ y GB'),
     ('give _ up', 'guiv *AP*', 'dejar (un hábito); rendirse', "Don't give up: the first month is the hardest.", 'No abandones: el primer mes es el más difícil.'),
     ('end up', 'end *AP*', 'terminar (sin haberlo planeado)', 'I ended up working in a café.', 'Terminé trabajando en un café.')]),
   ('A la vista y despierto', 'arriba = visible, activo', [
     ('show up', 'shou *AP*', 'aparecer, venir', "He didn't show up for his shift.", 'No vino a su turno.'),
     ('come up', 'kam *AP*', 'surgir', "Something came up: I can't come tonight.", 'Me surgió algo: hoy no puedo ir.'),
     ('look _ up', 'luk *AP*', 'buscar (en el diccionario)', "If you don't know a word, look it up.", 'Si no sabés una palabra, buscala.'),
     ('wake _ up', 'ueik *AP*', 'despertar(se)', 'Can you wake me up at five?', '¿Me despertás a las cinco?')])],
  practica=[f"Can you {H} the music {C}? I can't hear it.", f"Who {H} all the coffee? There's none left.",
            f"Don't {H}! Your English is getting better.", f"Sorry, I can't come. Something has {H}."],
  soluciones='a) turn the music up · b) used up · c) give up · d) come up',
  notas=[alerta('wake up no es get up.', '<span class="en">wake up</span> es despertarse; <span class="en">get up</span>, levantarse: <span class="en">I woke up at six, but got up at seven.</span>'),
         kiwi(SUST, [('a WARM-up', 'precalentamiento'), ('a SET-up', 'instalación, armado'), ('a BREAK-up', 'separación (de pareja)')])],
  fuentes="<i>wash up</i>: Oxford Learner's Dictionaries (en EE. UU. es lavarse las manos)."),

 dict(codigo='ING-PV-03', n=3, particula='down', pron='daun', titulo='DOWN: hacia abajo',
  bajada='Y de ahí: lo que disminuye, lo que queda fijo y lo que se viene abajo.',
  lateral='Su opuesto: UP, ING-PV-02', literal='De arriba hacia abajo, hasta el piso.',
  idea='Lo que baja es <b>menos</b>; lo que baja y se apoya queda <b>fijo</b> (anotado, en su lugar); lo que se viene abajo <b>falla</b> o <b>se rechaza</b>.',
  murphy='Murphy U142', ley_bien='write it down', ley_mal='write down it',
  ramas=[
   ('Hacia abajo', 'el sentido literal', [
     ('sit down', 'sit *DAUN*', 'sentarse', 'Please sit down, the manager is coming.', 'Sentate, ya viene el encargado.'),
     ('lie down', 'lai *DAUN*', 'acostarse (un rato)', 'I need to lie down for a bit.', 'Necesito acostarme un rato.'),
     ('put _ down', 'put *DAUN*', 'dejar, apoyar', 'Put the boxes down by the door.', 'Dejá las cajas al lado de la puerta.'),
     ('go down', 'gou *DAUN*', 'bajar', 'Go down the stairs and turn left.', 'Bajá la escalera y doblá a la izquierda.')]),
   ('Menos', 'abajo = menos cantidad', [
     ('slow down', 'slou *DAUN*', 'ir o hablar más despacio', "Slow down, please: I'm still learning.", 'Más despacio, por favor: todavía estoy aprendiendo.'),
     ('turn _ down', 'tern *DAUN*', 'bajar (volumen, calefacción)', 'Could you turn the music down?', '¿Podés bajar la música?'),
     ('cut down on _', 'kat *DAUN* on', 'consumir menos', "I'm cutting down on coffee.", 'Estoy tomando menos café.'),
     ('calm down', 'kaam *DAUN*', 'calmarse', "Calm down, we'll find your passport.", 'Calmate, vamos a encontrar tu pasaporte.')]),
   ('Fijo y anotado', 'abajo = quieto, registrado', [
     ('write _ down', 'rait *DAUN*', 'anotar', 'Could you write it down for me?', '¿Me lo anotás?'),
     ('hold _ down', 'jould *DAUN*', 'mantener (un trabajo)', "It's hard to hold down two jobs.", 'Es difícil sostener dos trabajos.'),
     ('track _ down', 'trak *DAUN*', 'ubicar (después de buscar)', 'I finally tracked down the landlord.', 'Por fin ubiqué al dueño.')]),
   ('Roto o rechazado', 'abajo = falla, no', [
     ('break down', 'breik *DAUN*', 'romperse (una máquina)', 'The van broke down near Taupō.', 'La camioneta se rompió cerca de Taupō.'),
     ('let _ down', 'let *DAUN*', 'fallarle a alguien', "Don't worry, I won't let you down.", 'No te preocupes, no te voy a fallar.'),
     ('turn _ down', 'tern *DAUN*', 'rechazar', 'She turned down the job: the pay was low.', 'Rechazó el trabajo: pagaban poco.'),
     ('shut _ down', 'shat *DAUN*', 'cerrar (del todo)', 'The factory shut down last year.', 'La fábrica cerró el año pasado.')])],
  practica=[f"Could you {H} the radio {C}, please?", f"Our van {H} on the way to Napier.",
            f"I'm trying to {H} on sugar.", f"Could you {H} your number {C} here?"],
  soluciones='a) turn the radio down · b) broke down · c) cut down · d) write your number down',
  notas=[alerta('Bajarse del colectivo no es get down.', 'Es <span class="en">get off the bus</span> (ING-PV-07). <span class="en">get down</span> es bajarse de algo alto o agacharse.'),
         kiwi(SUST, [('a BREAK-down', 'avería; crisis nerviosa'), ('a SHUT-down', 'cierre'), ('a COUNT-down', 'cuenta regresiva')])],
  fuentes="Sentidos de uso general (Oxford Learner's Dictionaries)."),

 dict(codigo='ING-PV-04', n=4, particula='in', pron='in', titulo='IN: hacia adentro',
  bajada='Y de ahí: entrar en un lugar o un sistema, agregar o entregar, y quedarse adentro.',
  lateral='Su opuesto: OUT, ING-PV-05', literal='De afuera hacia adentro de un recipiente.',
  idea='Un lugar, un grupo o un sistema también son <b>recipientes</b>: se entra (<span class="en">check in</span>), se agrega o se entrega algo (<span class="en">fill in</span>) y uno se queda adentro (<span class="en">stay in</span>).',
  murphy='Murphy U138', ley_bien='fill it in', ley_mal='fill in it',
  ramas=[
   ('Hacia adentro', 'el sentido literal', [
     ('come in', 'kam *IN*', 'entrar, pasar', "Come in, the door's open!", '¡Pasá, está abierto!'),
     ('get in', 'guet *IN*', 'subir (a un auto); llegar', "Get in, I'll give you a lift.", 'Subí, te llevo.'),
     ('move in', 'muuv *IN*', 'mudarse (a un lugar)', "I'm moving in on Saturday.", 'Me mudo el sábado.'),
     ('break in', 'breik *IN*', 'entrar a robar', 'Someone broke in last night.', 'Anoche entraron a robar.')]),
   ('Entrar en un sistema', 'registrarse, adaptarse', [
     ('check in', 'chek *IN*', 'registrarse (hotel, vuelo)', 'Can I check in early?', '¿Puedo hacer el check-in temprano?'),
     ('log in', 'log *IN*', 'entrar (a una cuenta)', "I can't log in to my bank app.", 'No puedo entrar a la app del banco.'),
     ('pop in', 'pop *IN*', 'pasar un momento', "Pop in any time, we're open till six.", 'Pasá cuando quieras: abrimos hasta las seis.', 'informal'),
     ('settle in', 'se-tl *IN*', 'adaptarse (a un lugar nuevo)', 'How are you settling in?', '¿Cómo te estás adaptando?')]),
   ('Agregar o entregar', 'adentro = incluido', [
     ('fill _ in', 'fil *IN*', 'completar (un formulario)', 'Please fill in this form.', 'Completá este formulario, por favor.', 'NZ y GB'),
     ('hand _ in', 'jand *IN*', 'entregar (al jefe, a una oficina)', 'Hand in your timesheet on Friday.', 'Entregá tu planilla de horas el viernes.'),
     ('plug _ in', 'plag *IN*', 'enchufar', 'Where can I plug in my phone?', '¿Dónde puedo enchufar el teléfono?'),
     ('join in', 'yoin *IN*', 'sumarse', "We're playing touch rugby: join in!", 'Estamos jugando al touch rugby: ¡sumate!')]),
   ('Quedarse o ceder', 'adentro = en casa', [
     ('stay in', 'stei *IN*', 'quedarse en casa', "It's raining: let's stay in tonight.", 'Llueve: quedémonos en casa esta noche.'),
     ('sleep in', 'sliip *IN*', 'dormir hasta tarde (a propósito)', 'On Sundays I sleep in.', 'Los domingos duermo hasta tarde.'),
     ('give in', 'guiv *IN*', 'ceder, rendirse', 'He kept asking, so I gave in.', 'Insistió tanto que cedí.')])],
  practica=[f"Where do I {H} for the flight to Christchurch?", f"My new flatmate is {H} on Monday.",
            f"Please {H} this form and give it back to me.", f"I'm tired: I think I'll {H} tonight."],
  soluciones='a) check in · b) moving in · c) fill in · d) stay in',
  notas=[alerta('Con el lugar, into.', '<span class="en">come in</span>, pero <span class="en">come into the kitchen</span>. Y nunca <span class="mal">enter in the room</span>: <span class="en">enter the room</span>.'),
         kiwi(SUST, [('a CHECK-in', 'mostrador de check-in'), ('a BREAK-in', 'robo con entrada forzada'), ('a LOG-in', 'usuario y clave')])],
  fuentes="<i>fill in</i>: Oxford Learner's Dictionaries (sobre todo en GB; <i>fill out</i> se usa en los dos lados)."),

 dict(codigo='ING-PV-05', n=5, particula='out', pron='aut', titulo='OUT: hacia afuera',
  bajada='Y de ahí: irse, acabarse, salir a la luz y resolver hasta el final.',
  lateral='Su opuesto: IN, ING-PV-04', literal='De adentro hacia afuera de un recipiente.',
  idea='Lo que sale <b>se va</b> o <b>se acaba</b>; lo que estaba guardado <b>sale a la luz</b>; y sacar todo afuera es <b>terminar</b> o resolver.',
  murphy='Murphy U138–139', ley_bien='sort it out', ley_mal='sort out it',
  ramas=[
   ('Hacia afuera', 'el sentido literal', [
     ('go out', 'gou *AUT*', 'salir (a divertirse)', 'Do you want to go out tonight?', '¿Querés salir esta noche?'),
     ('check out', 'chek *AUT*', 'dejar el hotel o el hostel', 'We have to check out by ten.', 'Tenemos que dejar el cuarto antes de las diez.'),
     ('move out', 'muuv *AUT*', 'mudarse (de un lugar)', 'When are you moving out?', '¿Cuándo te mudás?'),
     ('take _ out', 'teik *AUT*', 'sacar', 'Can you take the rubbish out?', '¿Podés sacar la basura?')]),
   ('Acabarse', 'afuera = ya no está', [
     ('run out of _', 'ran *AUT* ov', 'quedarse sin', "We've run out of milk.", 'Nos quedamos sin leche.'),
     ('sell out', 'sel *AUT*', 'agotarse', 'The tickets sold out in an hour.', 'Las entradas se agotaron en una hora.'),
     ('throw _ out', 'throu *AUT*', 'tirar (a la basura)', "Don't throw out the boxes.", 'No tires las cajas.'),
     ('pass out', 'paas *AUT*', 'desmayarse', 'It was so hot that a worker passed out.', 'Hacía tanto calor que un trabajador se desmayó.')]),
   ('A la luz', 'afuera = se sabe, se ve', [
     ('find out', 'faind *AUT*', 'enterarse, averiguar', 'I found out the job was taken.', 'Me enteré de que el puesto ya estaba ocupado.'),
     ('figure _ out', 'fi-gue *AUT*', 'entender, resolver', "I can't figure out this timetable.", 'No logro entender este horario.'),
     ('point _ out', 'point *AUT*', 'señalar, hacer notar', 'My boss pointed out a mistake.', 'Mi jefe me marcó un error.'),
     ('turn out', 'tern *AUT*', 'resultar', 'The job turned out to be great.', 'El trabajo resultó ser buenísimo.')]),
   ('Hasta el final', 'afuera = resuelto, repartido', [
     ('sort _ out', 'soot *AUT*', 'resolver, ordenar', "Don't worry, we'll sort it out.", 'No te preocupes, lo resolvemos.'),
     ('work out', 'uerk *AUT*', 'salir bien; entrenar', 'Things worked out in the end.', 'Al final todo salió bien.'),
     ('hand _ out', 'jand *AUT*', 'repartir', "They're handing out flyers.", 'Están repartiendo volantes.')])],
  practica=[f"We've {H} bread. Can you get some?", f"I can't {H} this bus timetable.",
            f"Don't worry: we'll {H} it {C}.", f"Can you {H} the rubbish {C} before you go?"],
  soluciones='a) run out of · b) figure out · c) sort it out · d) take the rubbish out',
  notas=[alerta('Irse del trabajo no es go out.', '<span class="en">go out</span> es salir a divertirse. Para irte de un lugar: <span class="en">I leave work at five</span>, no <span class="mal">I go out from work</span>.'),
         kiwi('En Nueva Zelanda', [('rubbish', 'basura'), ('takeaway', 'comida para llevar'), ('a WORK-out', 'una sesión de gimnasia')])],
  fuentes="Sentidos de uso general (Oxford Learner's Dictionaries)."),

 dict(codigo='ING-PV-06', n=6, particula='on', pron='on', titulo='ON: en contacto',
  bajada='Y de ahí: lo puesto, lo encendido, lo que sigue y aquello en lo que te apoyás.',
  lateral='Su opuesto: OFF, ING-PV-07', literal='Apoyado sobre una superficie, tocándola.',
  idea='Lo que queda en contacto está <b>puesto</b>; un circuito en contacto está <b>encendido</b>; no cortar el contacto es <b>seguir</b>; y lo apoyado <b>depende</b> de su base.',
  murphy='Murphy U140–141', ley_bien='put them on', ley_mal='put on them',
  ramas=[
   ('Puesto encima', 'el sentido literal', [
     ('put _ on', 'put *ON*', 'ponerse (ropa)', "Put your boots on: it's a building site.", 'Ponete las botas: es una obra.'),
     ('try _ on', 'trai *ON*', 'probarse', 'Can I try these on?', '¿Me los puedo probar?'),
     ('get on', 'guet *ON*', 'subir (al colectivo, al tren)', 'We got on the wrong bus.', 'Nos subimos al colectivo equivocado.')]),
   ('Encendido', 'en contacto = funciona', [
     ('turn _ on', 'tern *ON*', 'prender (luz, máquina)', 'Turn the lights on, please.', 'Prendé las luces, por favor.'),
     ('put the kettle on', 'put the ke-tl *ON*', 'poner la pava', "I'll put the kettle on: tea or coffee?", 'Pongo la pava: ¿té o café?'),
     ('come on', 'kam *ON*', 'prenderse; ¡dale!', "Come on, we're late!", '¡Dale, que llegamos tarde!')]),
   ('Seguir', 'en contacto = sin cortar', [
     ('carry on', 'ka-ri *ON*', 'seguir (haciendo algo)', "Carry on, I'll be back in a minute.", 'Seguí, ya vuelvo.'),
     ('go on', 'gou *ON*', 'seguir; pasar', "What's going on?", '¿Qué está pasando?'),
     ('hold on', 'jould *ON*', 'esperar un momento', "Hold on, I'll get the manager.", 'Esperá, llamo al encargado.'),
     ('move on', 'muuv *ON*', 'pasar a otra cosa', "Let's move on to the next job.", 'Pasemos a la próxima tarea.'),
     ('get on with _', 'guet *ON* uith', 'llevarse bien con', 'I get on well with my flatmates.', 'Me llevo bien con mis compañeros de casa.')]),
   ('Apoyarse', 'en contacto = depender, cargar', [
     ('rely on _', 'ri-*LAI* on', 'contar con, depender de', 'You can rely on me.', 'Podés contar conmigo.'),
     ('depend on _', 'di-*PEND* on', 'depender de', 'It depends on the weather.', 'Depende del clima.'),
     ('take _ on', 'teik *ON*', 'contratar; asumir (una tarea)', "They're taking on staff for summer.", 'Están tomando personal para el verano.')])],
  practica=[f"It's cold: {H} your jacket {C}.", f"{H}, I'm on the phone.",
            f"Can I {H} these jeans {C}?", f"I {H} well with my boss."],
  soluciones='a) put your jacket on · b) Hold on · c) try these jeans on · d) get on',
  notas=[alerta('put on no es wear.', '<span class="en">put on</span> es la acción (ponerse); <span class="en">wear</span>, el estado (llevar puesto): <span class="en">I put on my boots. Now I\'m wearing them.</span>'),
         kiwi('Dónde cae el acento', [('turn it ON', 'phrasal verb: suena la partícula'), ('ri-LAI on me', 'verbo + preposición: suena el verbo')])],
  fuentes="<i>get on with</i>: Oxford Learner's Dictionaries (en EE. UU., <i>get along with</i>)."),

 dict(codigo='ING-PV-07', n=7, particula='off', pron='of', titulo='OFF: separado',
  bajada='Y de ahí: irse o arrancar, apagar o cancelar, y terminar con algo.',
  lateral='Su opuesto: ON, ING-PV-06', literal='Lo que estaba apoyado se despega y se aleja.',
  idea='Separarse es <b>irse</b> o <b>arrancar</b>; un circuito separado está <b>apagado</b>; y sacarse algo de encima es <b>terminar</b> con eso.',
  murphy='Murphy U140–141', ley_bien='turn it off', ley_mal='turn off it',
  ramas=[
   ('Separarse', 'el sentido literal', [
     ('take _ off', 'teik *OF*', 'sacarse (ropa)', 'Take your shoes off at the door.', 'Sacate los zapatos en la puerta.'),
     ('get off', 'guet *OF*', 'bajarse (del colectivo, del tren)', 'Get off at the next stop.', 'Bajate en la próxima parada.'),
     ('drop _ off', 'drop *OF*', 'dejar (a alguien en un lugar)', 'Can you drop me off at the station?', '¿Me dejás en la estación?'),
     ('take off', 'teik *OF*', 'despegar (un avión)', 'The plane takes off at 6:40.', 'El avión despega a las 6:40.')]),
   ('Irse, arrancar', 'separarse = partir', [
     ('set off', 'set *OF*', 'salir (de viaje)', 'We set off early to avoid the traffic.', 'Salimos temprano para evitar el tránsito.'),
     ('head off', 'jed *OF*', 'irse', "I'm heading off, see you tomorrow.", 'Me voy, nos vemos mañana.'),
     ('go off', 'gou *OF*', 'sonar (una alarma)', "My alarm didn't go off.", 'No me sonó la alarma.')]),
   ('Apagar, cancelar', 'separado = sin conexión', [
     ('turn _ off', 'tern *OF*', 'apagar', 'Turn off the lights when you leave.', 'Apagá las luces cuando te vayas.'),
     ('call _ off', 'kool *OF*', 'suspender, cancelar', 'They called off the match: too much rain.', 'Suspendieron el partido: llovía demasiado.'),
     ('put _ off', 'put *OF*', 'posponer', "Don't put off your IRD application.", 'No postergues el trámite del IRD.'),
     ('lay _ off', 'lei *OF*', 'despedir (por falta de trabajo)', 'The company laid off twenty workers.', 'La empresa despidió a veinte trabajadores.')]),
   ('Terminar', 'sacarse algo de encima', [
     ('knock off', 'nok *OF*', 'terminar de trabajar', 'What time do you knock off?', '¿A qué hora salís del trabajo?', 'informal'),
     ('finish _ off', 'fi-nish *OF*', 'terminar (lo último)', "I'll finish off this wall and go home.", 'Termino esta pared y me voy.'),
     ('pay off', 'pei *OF*', 'dar resultado', 'All that studying paid off.', 'Todo ese estudio valió la pena.')])],
  practica=[f"Could you {H} the heater {C}? It's too hot.", f"We {H} at four on Fridays.",
            f"The game was {H} because of the storm.", f"{H} the bus at the museum."],
  soluciones='a) turn the heater off · b) knock off · c) called off · d) Get off',
  notas=[alerta('off no es of.', '<span class="en">off</span> termina en f fuerte; <span class="en">of</span> suena casi «ov»: <span class="en">a day off</span> (un día libre), no <span class="mal">a day of</span>.'),
         kiwi('En el trabajo, en Nueva Zelanda', [('smoko', 'descanso para el té'), ('a day off', 'un día libre'), ('go off', 'echarse a perder (comida)')])],
  fuentes="<i>knock off</i>, <i>go off</i>: Oxford Learner's Dictionaries. <i>smoko</i>: NZ y Australia (guías de inglés kiwi)."),

 dict(codigo='ING-PV-08', n=8, particula='back', pron='bak', titulo='BACK: de vuelta',
  bajada='Y de ahí: devolver, responder, frenar y recordar. Abajo, su pareja: AWAY.',
  lateral='Pareja: AWAY (en esta hoja)', literal='Volver al punto de partida.',
  idea='Lo que vuelve a su dueño se <b>devuelve</b>; una palabra que vuelve es una <b>respuesta</b>; ir hacia atrás es <b>frenar</b> o <b>recordar</b>.',
  murphy='Murphy U145', ley_bien='give it back', ley_mal='give back it',
  ramas=[
   ('Volver', 'el sentido literal', [
     ('come back', 'kam *BAK*', 'volver (acá)', "I'll come back tomorrow with my passport.", 'Vuelvo mañana con el pasaporte.'),
     ('go back', 'gou *BAK*', 'volver (allá)', 'I want to go back to the South Island.', 'Quiero volver a la Isla Sur.'),
     ('get back', 'guet *BAK*', 'volver, llegar de vuelta', 'What time did you get back last night?', '¿A qué hora volviste anoche?'),
     ('be back', 'bii *BAK*', 'estar de vuelta', "I'll be back in five minutes.", 'Vuelvo en cinco minutos.')]),
   ('Devolver', 'a su dueño o a su lugar', [
     ('give _ back', 'guiv *BAK*', 'devolver', 'Can you give me my charger back?', '¿Me devolvés el cargador?'),
     ('pay _ back', 'pei *BAK*', 'devolver (plata)', "I'll pay you back on Friday.", 'Te devuelvo la plata el viernes.'),
     ('take _ back', 'teik *BAK*', 'devolver (a una tienda)', 'I took the shoes back: too small.', 'Devolví los zapatos: me quedaban chicos.'),
     ('put _ back', 'put *BAK*', 'volver a dejar en su lugar', 'Put the tools back when you finish.', 'Guardá las herramientas cuando termines.')]),
   ('Responder', 'la palabra vuelve', [
     ('call _ back', 'kool *BAK*', 'devolver la llamada', 'Can I call you back in ten minutes?', '¿Te llamo en diez minutos?'),
     ('get back to _', 'guet *BAK* tu', 'responderle a alguien (después)', "I'll get back to you by Monday.", 'Te respondo antes del lunes.')]),
   ('Frenar, recordar', 'hacia atrás', [
     ('cut back on _', 'kat *BAK* on', 'recortar (gastos)', 'We need to cut back on spending.', 'Tenemos que recortar gastos.'),
     ('look back', 'luk *BAK*', 'mirar hacia atrás, recordar', 'Looking back, it was the best year.', 'Mirando hacia atrás, fue el mejor año.')])],
  pareja='''    <div class="pareja">
      <svg class="esquema" data-particula="away"></svg>
      <div>
        <span class="h3">Su pareja: AWAY, lejos <span class="pron">(a-<span class="tonica">UEI</span>)</span> <span class="ref">Murphy U145</span></span>
        <div class="lista">
          <span><span class="pv">go away</span> — irse lejos; ¡andate!</span>
          <span><span class="pv">put <i class="obj"></i> away</span> — guardar (en su lugar)</span>
          <span><span class="pv">throw <i class="obj"></i> away</span> — tirar (a la basura)</span>
          <span><span class="pv">give <i class="obj"></i> away</span> — regalar</span>
          <span><span class="pv">get away</span> — escaparse; irse unos días</span>
          <span><span class="pv">take <i class="obj"></i> away</span> — llevarse; de ahí, <span class="en">takeaway</span></span>
        </div>
      </div>
    </div>''',
  practica=[f"I'll {H} to you tomorrow with the details.", f"Can you {H} me {C} by Friday?",
            f"I missed your call. I'll {H} you {C} after work.", f"{H} your clothes {C} before the inspection."],
  soluciones='a) get back · b) pay me back · c) call you back · d) Put … away',
  notas=[alerta('return ya incluye back.', 'No digas <span class="mal">return back</span>: alcanza con <span class="en">return</span>, o <span class="en">give back</span>, <span class="en">come back</span>.'),
         kiwi(SUST, [('a BACK-up', 'copia de seguridad; respaldo'), ('a CUT-back', 'recorte'), ('a TAKE-away', 'comida para llevar')])],
  fuentes='Murphy, <i>English Grammar in Use</i>, 5.ª ed., U145 (away/back).'),

 dict(codigo='ING-PV-09', n=9, particula='over', pron='*OU*-va', titulo='OVER: por encima',
  bajada='Y de ahí: caer, pasar al otro lado, repasar y superar.',
  lateral='Sin opuesto directo', literal='Por encima de algo, de un lado al otro.',
  idea='Pasar al otro lado es <b>visitar</b> o <b>entregar</b>; pasar la vista por encima es <b>repasar</b>; dejar atrás el obstáculo es <b>superarlo</b>; y lo que se vuelca, <b>se cae</b>.',
  murphy='Murphy: sin unidad propia', ley_bien='think it over', ley_mal='think over it',
  ramas=[
   ('Por encima, al caer', 'el sentido literal', [
     ('fall over', 'fool *OU*-va', 'caerse', "Mind the step, you'll fall over.", 'Cuidado con el escalón, te vas a caer.'),
     ('knock _ over', 'nok *OU*-va', 'volcar, tirar (sin querer)', 'I knocked over a glass of water.', 'Volqué un vaso de agua.'),
     ('turn _ over', 'tern *OU*-va', 'dar vuelta', 'Turn the steaks over now.', 'Ahora dales vuelta a los bifes.')]),
   ('Al otro lado', 'visitar, pasar a otro', [
     ('come over', 'kam *OU*-va', 'venir (a tu casa)', 'Do you want to come over for dinner?', '¿Querés venir a cenar?'),
     ('sleep over', 'sliip *OU*-va', 'quedarse a dormir', 'You can sleep over on the couch.', 'Podés quedarte a dormir en el sillón.'),
     ('hand _ over', 'jand *OU*-va', 'entregar', 'Hand over the keys when you leave.', 'Entregá las llaves cuando te vayas.'),
     ('take _ over', 'teik *OU*-va', 'hacerse cargo, reemplazar', 'Can you take over? I need a break.', '¿Me reemplazás? Necesito un descanso.')]),
   ('Repasar', 'la vista pasa por encima', [
     ('look _ over', 'luk *OU*-va', 'revisar (rápido)', 'Could you look over my CV?', '¿Me revisás el CV?'),
     ('go over _', 'gou *OU*-va', 'repasar', "Let's go over the safety rules.", 'Repasemos las normas de seguridad.'),
     ('think _ over', 'think *OU*-va', 'pensarlo bien', 'Can I think it over until tomorrow?', '¿Lo puedo pensar hasta mañana?'),
     ('talk _ over', 'took *OU*-va', 'charlar algo (para decidir)', "Let's talk it over with the team.", 'Charlémoslo con el equipo.')]),
   ('Superar, terminar', 'el obstáculo quedó atrás', [
     ('get over _', 'guet *OU*-va', 'superar, recuperarse de', 'It took me a week to get over the jet lag.', 'Tardé una semana en recuperarme del jet lag.'),
     ('be over', 'bii *OU*-va', 'terminar', 'Summer is over: time to find winter work.', 'Se terminó el verano: hay que buscar trabajo de invierno.')])],
  practica=[f"Could you {H} my cover letter before I send it?", f"It took me ages to {H} the flu.",
            f"Why don't you {H} on Saturday?", f"Let me {H} it {C} and I'll call you tomorrow."],
  soluciones='a) look over · b) get over · c) come over · d) think it over',
  notas=[alerta('over no es on.', '<span class="en">on</span> es apoyado; <span class="en">over</span>, por encima sin tocar, o cubriendo: <span class="en">the lamp over the table</span>, <span class="en">the cup on the table</span>.'),
         kiwi(SUST, [('a TAKE-over', 'compra de una empresa'), ('a HANG-over', 'resaca'), ('a SLEEP-over', 'pijamada')])],
  fuentes='El Murphy solo nombra <i>over</i> en la U137 (introducción).'),
]

for h in HOJAS:
    with open(f"{DESTINO}/{h['codigo']}.html", 'w') as f:
        f.write(hoja(h))
print('ok', len(HOJAS))
