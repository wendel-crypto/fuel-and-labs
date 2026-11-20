# Builds site/case-page.html (the Fuel & Labs case study at wendelfreitas.com/fuel-and-labs/)
# and site/cases-app-card.snippet.html. English is baked in; Spanish and Portuguese swap in from C.
import json, pathlib, html

root = pathlib.Path(__file__).resolve().parent.parent
R = 'https://raw.githubusercontent.com/wendel-crypto/fuel-and-labs/main/docs/'
APP = '/fuel-and-labs/app/'
C = {
'title': ['Fuel & Labs — Nutrition and lab results apps case study | Wendel Freitas', 'Fuel & Labs — Caso de estudio de apps de nutrición y análisis | Wendel Freitas', 'Fuel & Labs — Case de apps de nutrição e exames | Wendel Freitas'],
'back': ['← Cases / App', '← Casos / App', '← Cases / App'],
'eyebrow': ['Personal product · Web apps · Health + AI agents', 'Producto personal · Apps web · Salud + agentes de IA', 'Produto pessoal · Apps web · Saúde + agentes de IA'],
'lede': ['Two companion apps for a marathon build. Fuel turns every training day into carbs, protein, meals, recipes and a weekly grocery cart. Labs turns seven blood panels into one clear view of what to fix. Built with Claude, fed by Garmin and kept fresh by scheduled agents.',
         'Dos apps complementarias para preparar un maratón. Fuel convierte cada día de entrenamiento en carbohidratos, proteína, comidas, recetas y un carrito semanal. Labs convierte siete análisis de sangre en una vista clara de lo que hay que corregir. Hechas con Claude, alimentadas por Garmin y actualizadas por agentes programados.',
         'Dois apps complementares para a preparação de uma maratona. O Fuel transforma cada dia de treino em carboidratos, proteína, refeições, receitas e um carrinho semanal. O Labs transforma sete exames de sangue em uma visão clara do que corrigir. Feitos com Claude, alimentados pelo Garmin e atualizados por agentes agendados.'],
'b1': ['Try the apps ↓', 'Prueba las apps ↓', 'Teste os apps ↓'], 'b2': ['Open full screen', 'Pantalla completa', 'Tela cheia'], 'b3': ['View the code ↗', 'Ver el código ↗', 'Ver o código ↗'],
'f1': ['Training days planned', 'Días de entrenamiento planificados', 'Dias de treino planejados'], 'f2': ['Meals with recipes', 'Comidas con receta', 'Refeições com receita'],
'f3': ['Lab markers tracked', 'Marcadores seguidos', 'Marcadores acompanhados'], 'f4': ['Scheduled agents', 'Agentes programados', 'Agentes agendados'],
'pe': ['The problem', 'El problema', 'O problema'],
'ph': ['A training plan says how far. It never says what to eat.', 'Un plan de entrenamiento dice cuánto correr. Nunca qué comer.', 'Uma planilha de treino diz quanto correr. Nunca o que comer.'],
'p1': ['Marathon fueling is arithmetic most runners skip: grams of carbohydrate per kilo of body weight, different for a rest day, a 5:30 am track session and a 32 km long run, with top-ups before the big days and a carb load before the race. Doing it by hand every day does not last.',
       'La alimentación para un maratón es aritmética que casi todos se saltan: gramos de carbohidrato por kilo de peso, distintos para un día de descanso, una pista a las 5:30 y un fondo de 32 km, con refuerzos antes de los días grandes y carga de carbohidratos antes de la carrera. Hacerlo a mano cada día no dura.',
       'A nutrição para maratona é uma conta que quase todo mundo pula: gramas de carboidrato por quilo de peso, diferentes para um dia de descanso, uma pista às 5h30 e um longão de 32 km, com reforço antes dos dias grandes e carga de carboidrato antes da prova. Fazer isso à mão todo dia não dura.'],
'p2': ['Blood work has the opposite problem: plenty of numbers, no story. Seven PDFs from two labs over three years, each with its own layout and units, and no easy way to see which markers are drifting and what to ask the doctor.',
       'Los análisis de sangre tienen el problema contrario: muchos números y ninguna historia. Siete PDF de dos laboratorios en tres años, cada uno con su formato y unidades, y ninguna forma fácil de ver qué marcadores se desvían y qué preguntarle al médico.',
       'Os exames de sangue têm o problema oposto: muitos números e nenhuma história. Sete PDFs de dois laboratórios em três anos, cada um com seu layout e unidades, e nenhum jeito fácil de ver quais marcadores estão saindo do lugar e o que perguntar ao médico.'],
'p3': ['So the two apps share one job: read the data that already exists and say what to do today.', 'Así que las dos apps comparten una tarea: leer los datos que ya existen y decir qué hacer hoy.', 'Então os dois apps têm uma mesma tarefa: ler os dados que já existem e dizer o que fazer hoje.'],
'te': ['Interactive apps', 'Apps interactivas', 'Apps interativos'], 'th': ['Use them right here.', 'Úsalas aquí mismo.', 'Use aqui mesmo.'],
'tp': ['These are the working apps with sample data, not videos. Pick a day in Fuel’s hero, open a recipe, tap a week in the build; in Labs, hover the heatmap or pick any marker to chart it.',
       'Son las apps reales con datos de ejemplo, no videos. Elige un día en la portada de Fuel, abre una receta, toca una semana del plan; en Labs, recorre el mapa de calor o elige cualquier marcador para graficarlo.',
       'São os apps de verdade com dados de exemplo, não vídeos. Escolha um dia no topo do Fuel, abra uma receita, toque em uma semana do plano; no Labs, passe pelo mapa de calor ou escolha qualquer marcador para ver o gráfico.'],
'tf': ['Fuel', 'Fuel', 'Fuel'], 'tl': ['Labs', 'Labs', 'Labs'],
'note': ['Sample data · 70 kg demo athlete · lab values shifted from the originals · not medical advice', 'Datos de ejemplo · atleta demo de 70 kg · valores de laboratorio alterados · no es consejo médico', 'Dados de exemplo · atleta demo de 70 kg · valores de exame alterados · não é orientação médica'],
'mopen': ['Open Fuel & Labs', 'Abrir Fuel & Labs', 'Abrir Fuel & Labs'],
'se': ['Screens', 'Pantallas', 'Telas'], 'sh': ['Two apps, one design system, light and dark.', 'Dos apps, un sistema de diseño, claro y oscuro.', 'Dois apps, um design system, claro e escuro.'],
'me': ['On the phone', 'En el teléfono', 'No celular'], 'mh': ['Built for the 5 am check before the run.', 'Pensadas para el vistazo de las 5 am antes de correr.', 'Pensados para a olhada das 5h antes de correr.'],
'mp': ['Both apps install to the home screen and open full screen. The day strip, macros and weather fit above the fold on a phone; meals stack into photo cards with the recipe one tap away.',
       'Las dos apps se instalan en la pantalla de inicio y abren a pantalla completa. La tira de días, los macros y el clima caben sin desplazarse en el teléfono; las comidas se apilan en tarjetas con foto y la receta a un toque.',
       'Os dois apps vão para a tela inicial e abrem em tela cheia. A faixa de dias, os macros e o clima cabem sem rolar no celular; as refeições viram cartões com foto e a receita fica a um toque.'],
'he': ['How it runs', 'Cómo funciona', 'Como funciona'], 'hh': ['Data in, decisions out, agents in between.', 'Datos que entran, decisiones que salen, agentes en el medio.', 'Dados entrando, decisões saindo, agentes no meio.'],
'h1h': ['Garmin sets the targets', 'Garmin define las metas', 'O Garmin define as metas'], 'h1': ['The private version reads the median of the last ten Garmin weigh-ins, so carbs, protein and fat move with body weight instead of a number typed once.', 'La versión privada lee la mediana de los últimos diez pesajes de Garmin, así los macros cambian con el peso real y no con un número escrito una vez.', 'A versão privada lê a mediana das últimas dez pesagens do Garmin, então os macros acompanham o peso real e não um número digitado uma vez.'],
'h2h': ['The plan drives the menu', 'El plan decide el menú', 'O plano decide o cardápio'], 'h2': ['Each of 154 days has a session type and distance. Rules turn it into grams per kilo, add a top-up before long runs of 24 km or more and a 10 g/kg carb load for the last three days.', 'Cada uno de los 154 días tiene tipo de sesión y distancia. Las reglas lo convierten en gramos por kilo, suman refuerzo antes de fondos de 24 km o más y carga de 10 g/kg los tres últimos días.', 'Cada um dos 154 dias tem tipo de treino e distância. As regras viram gramas por quilo, somam reforço antes de longões de 24 km ou mais e carga de 10 g/kg nos três últimos dias.'],
'h3h': ['A Friday grocery agent', 'Un agente de compras los viernes', 'Um agente de compras às sextas'], 'h3': ['Every Friday at 7:40 am a scheduled Claude task reads next week’s sessions, fills an Instacart cart and sends the link. Checkout stays with the human; nothing is bought automatically.', 'Cada viernes a las 7:40 una tarea programada de Claude lee las sesiones de la semana siguiente, llena un carrito de Instacart y envía el enlace. El pago lo hace la persona; nada se compra solo.', 'Toda sexta às 7h40 uma tarefa agendada do Claude lê os treinos da semana seguinte, enche um carrinho no Instacart e manda o link. O pagamento fica com a pessoa; nada é comprado sozinho.'],
'h4h': ['A 4 am weather agent', 'Un agente del clima a las 4 am', 'Um agente do clima às 4h'], 'h4': ['A daily task saves the Miami forecast before the run. The morning low becomes a fluid tip: humid starts get 500 ml more and an extra electrolyte stick.', 'Una tarea diaria guarda el pronóstico de Miami antes de correr. La mínima de la mañana se vuelve un consejo de hidratación: madrugadas húmedas suman 500 ml y un electrolito extra.', 'Uma tarefa diária salva a previsão de Miami antes da corrida. A mínima da manhã vira uma dica de hidratação: madrugadas úmidas ganham 500 ml e um eletrólito a mais.'],
'h5h': ['Seven PDFs, one table', 'Siete PDF, una tabla', 'Sete PDFs, uma tabela'], 'h5': ['Claude read seven lab reports from two labs and normalized them into one table: marker, date, value, unit, lab range and flag. Everything in Labs is drawn from that file.', 'Claude leyó siete informes de dos laboratorios y los unificó en una tabla: marcador, fecha, valor, unidad, rango y alerta. Todo en Labs sale de ese archivo.', 'O Claude leu sete laudos de dois laboratórios e unificou tudo em uma tabela: marcador, data, valor, unidade, faixa e alerta. Tudo no Labs sai desse arquivo.'],
'h6h': ['Athlete targets, not just lab ranges', 'Metas de atleta, no solo rangos', 'Metas de atleta, não só faixas do laboratório'], 'h6': ['A value can be inside the lab range and still worth watching for an endurance athlete. Labs adds a second, stricter target and a separate amber state for it.', 'Un valor puede estar dentro del rango y aun así merecer atención en un atleta de resistencia. Labs agrega una meta más estricta y un estado ámbar propio.', 'Um valor pode estar dentro da faixa e ainda assim merecer atenção em um atleta de endurance. O Labs adiciona uma meta mais rígida e um estado âmbar próprio.'],
'de': ['Design decisions', 'Decisiones de diseño', 'Decisões de design'], 'dh': ['Six choices that make the numbers readable at a glance.', 'Seis decisiones para leer los números de un vistazo.', 'Seis escolhas para ler os números de relance.'],
'd1h': ['The date is the headline', 'La fecha es el titular', 'A data é a manchete'], 'd1': ['A 128-pixel day number, the weekday and the session sit first, so the app answers “what is today” before anything else.', 'Un número de día de 128 píxeles, el día y la sesión van primero, así la app responde “qué toca hoy” antes que nada.', 'Um número do dia com 128 pixels, o dia da semana e o treino vêm primeiro, então o app responde “o que tem hoje” antes de tudo.'],
'd2h': ['The week lives inside the hero', 'La semana vive en la portada', 'A semana mora no topo'], 'd2': ['Seven day tiles with an icon and kilometers sit in the hero, so changing day never scrolls the page.', 'Siete casillas con ícono y kilómetros viven en la portada, así cambiar de día nunca mueve la página.', 'Sete blocos com ícone e quilômetros ficam no topo, então trocar de dia nunca rola a página.'],
'd3h': ['Weeks, not 154 bars', 'Semanas, no 154 barras', 'Semanas, não 154 barras'], 'd3': ['The first draft charted every day and was unreadable. The build is now 22 rows grouped by phase: weekly kilometers as a bar, average carbs as a number, the long run on the right.', 'El primer borrador graficaba cada día y era ilegible. Ahora son 22 filas por fase: kilómetros semanales en barra, carbohidratos promedio en número y el fondo a la derecha.', 'O primeiro rascunho mostrava cada dia e era ilegível. Agora são 22 linhas por fase: quilômetros na barra, média de carboidrato em número e o longão à direita.'],
'd4h': ['Food you can see', 'Comida que se ve', 'Comida que dá para ver'], 'd4': ['Every meal has a photo, a time, macro chips and a folded recipe with prep minutes. Dishes are AI-generated; juices are Unsplash photos, credited on the card.', 'Cada comida tiene foto, hora, chips de macros y una receta plegada con minutos de preparación. Los platos son generados con IA; los jugos son fotos de Unsplash, con crédito.', 'Cada refeição tem foto, horário, chips de macros e uma receita recolhida com tempo de preparo. Os pratos são gerados por IA; os sucos são fotos do Unsplash, com crédito.'],
'd5h': ['Three states, one legend', 'Tres estados, una leyenda', 'Três estados, uma legenda'], 'd5': ['Labs uses red for flagged by the lab, amber for outside the athlete target and green for in range, in the ring, the heatmap, the cards and the charts alike.', 'Labs usa rojo para lo marcado por el laboratorio, ámbar para fuera de la meta de atleta y verde para lo que está en rango, igual en el anillo, el mapa de calor, las tarjetas y los gráficos.', 'O Labs usa vermelho para o que o laboratório marcou, âmbar para fora da meta de atleta e verde para dentro da faixa, igual no anel, no mapa de calor, nos cartões e nos gráficos.'],
'd6h': ['Every number shows its source', 'Cada número muestra su origen', 'Cada número mostra a origem'], 'd6': ['In the private dashboards each figure links back to the row or calculation it came from, so a coach or a doctor can check it.', 'En los paneles privados cada cifra enlaza a la fila o el cálculo de donde salió, para que un entrenador o un médico lo verifique.', 'Nos painéis privados cada número leva à linha ou ao cálculo de onde veio, para um treinador ou um médico conferir.'],
'ye': ['Design system', 'Sistema de diseño', 'Design system'], 'yh': ['Ocean navy, one working blue, sans-serif throughout.', 'Azul marino océano, un azul de acción, sans-serif en todo.', 'Azul-marinho oceano, um azul de ação, sans-serif em tudo.'],
'y1': ['The palette moved from forest green to ocean blue to match Miami mornings: a navy-to-teal gradient for heroes, blue for actions, teal for hydration, amber for carbs and a fixed set of session colors (teal easy, violet track, blue long run, coral race).',
       'La paleta pasó de verde bosque a azul océano, como las mañanas de Miami: un degradado de azul marino a turquesa en las portadas, azul para acciones, turquesa para hidratación, ámbar para carbohidratos y colores fijos por sesión (turquesa suave, violeta pista, azul fondo, coral carrera).',
       'A paleta saiu do verde floresta para o azul oceano, como as manhãs de Miami: um degradê de azul-marinho a turquesa nos topos, azul para ações, turquesa para hidratação, âmbar para carboidrato e cores fixas por treino (turquesa leve, violeta pista, azul longão, coral prova).'],
'y2': ['Type is Inter from 10 to 128 pixels with tabular figures for every number. Both apps follow the system light or dark setting, and every section works on a 390-pixel phone.',
       'La tipografía es Inter de 10 a 128 píxeles con cifras tabulares en cada número. Las dos apps siguen el modo claro u oscuro del sistema, y cada sección funciona en un teléfono de 390 píxeles.',
       'A tipografia é Inter de 10 a 128 pixels com algarismos tabulares em todo número. Os dois apps seguem o modo claro ou escuro do sistema, e cada seção funciona em um celular de 390 pixels.'],
're': ['My role', 'Mi rol', 'Meu papel'], 'rh': ['Product, art direction and data. Built with Claude.', 'Producto, dirección de arte y datos. Construido con Claude.', 'Produto, direção de arte e dados. Construído com Claude.'],
'r1': ['I set the brief, the fueling rules and the visual direction, and reviewed every iteration, from the first green dashboard to the blue redesign. Claude read the lab reports, wrote the apps, generated the dish images and runs the Friday and morning agents.',
       'Definí el brief, las reglas de alimentación y la dirección visual, y revisé cada iteración, del primer panel verde al rediseño azul. Claude leyó los informes, escribió las apps, generó las imágenes de los platos y ejecuta los agentes de los viernes y de la mañana.',
       'Defini o briefing, as regras de nutrição e a direção visual, e revisei cada iteração, do primeiro painel verde ao redesenho azul. O Claude leu os laudos, escreveu os apps, gerou as imagens dos pratos e roda os agentes de sexta e da manhã.'],
'r2': ['The public build uses sample data: a 70 kg demo athlete and lab values shifted from the originals. It is a design and product case, not medical advice.',
       'La versión pública usa datos de ejemplo: un atleta demo de 70 kg y valores de laboratorio alterados. Es un caso de diseño y producto, no consejo médico.',
       'A versão pública usa dados de exemplo: um atleta demo de 70 kg e valores de exame alterados. É um case de design e produto, não orientação médica.'],
'foot': ['Designed and directed by Wendel Freitas · written with Claude', 'Diseñado y dirigido por Wendel Freitas · escrito con Claude', 'Desenhado e dirigido por Wendel Freitas · escrito com Claude'],
}
S = [('fuel-desktop', ['Fuel · today', 'Fuel · hoy', 'Fuel · hoje'], ['Big date, session and distance, Miami weather with a fluid tip, the week strip and the day’s carbs, protein, fat and energy.', 'Fecha grande, sesión y distancia, clima de Miami con consejo de hidratación, la semana y los carbohidratos, proteína, grasa y energía del día.', 'Data grande, treino e distância, clima de Miami com dica de hidratação, a semana e os carboidratos, proteína, gordura e energia do dia.']),
     ('fuel-meals', ['Fuel · menu', 'Fuel · menú', 'Fuel · cardápio'], ['The day’s meals as photo cards with times, macro chips and a recipe that unfolds.', 'Las comidas del día en tarjetas con foto, horarios, macros y una receta que se despliega.', 'As refeições do dia em cartões com foto, horários, macros e uma receita que abre.']),
     ('fuel-build', ['Fuel · the build', 'Fuel · el plan', 'Fuel · o plano'], ['Twenty-two weeks by phase: weekly kilometers, average carbs per day and the long run. Tap a week to plan it.', 'Veintidós semanas por fase: kilómetros, carbohidratos promedio por día y el fondo. Toca una semana para planificarla.', 'Vinte e duas semanas por fase: quilômetros, média de carboidrato por dia e o longão. Toque em uma semana para planejá-la.']),
     ('fuel-juices', ['Fuel · juice bar', 'Fuel · jugos', 'Fuel · sucos'], ['A juice for each kind of day, with when to drink it, the carbs and why it helps.', 'Un jugo para cada tipo de día, con cuándo tomarlo, los carbohidratos y por qué ayuda.', 'Um suco para cada tipo de dia, com quando tomar, os carboidratos e por que ajuda.']),
     ('fuel-shop', ['Fuel · groceries', 'Fuel · compras', 'Fuel · compras']),
     ('fuel-dark', ['Fuel · dark mode', 'Fuel · modo oscuro', 'Fuel · modo escuro'], ['A long-run Sunday in dark mode: the same hierarchy on navy.', 'Un domingo de fondo en modo oscuro: la misma jerarquía sobre azul marino.', 'Um domingo de longão no modo escuro: a mesma hierarquia sobre azul-marinho.']),
     ('labs-desktop', ['Labs · overview', 'Labs · resumen', 'Labs · visão geral'], ['A one-line verdict, a ring of 42 markers by state and the four markers that matter most.', 'Un veredicto en una línea, un anillo con 42 marcadores por estado y los cuatro que más importan.', 'Um veredito em uma linha, um anel com 42 marcadores por estado e os quatro que mais importam.']),
     ('labs-heatmap', ['Labs · heatmap', 'Labs · mapa de calor', 'Labs · mapa de calor'], ['Every result from every draw in one grid, grouped by body system and colored by state.', 'Cada resultado de cada análisis en una grilla, agrupado por sistema y coloreado por estado.', 'Cada resultado de cada exame em uma grade, agrupado por sistema e colorido por estado.']),
     ('labs-systems', ['Labs · body systems', 'Labs · sistemas', 'Labs · sistemas']),
     ('labs-explore', ['Labs · explore and act', 'Labs · explorar y actuar', 'Labs · explorar e agir'], ['Chart any marker against the lab range and the athlete target, then a plan for this week, the next eight and the retest.', 'Grafica cualquier marcador contra el rango y la meta de atleta, y luego un plan para esta semana, las próximas ocho y el nuevo análisis.', 'Veja qualquer marcador contra a faixa e a meta de atleta, e depois um plano para esta semana, as próximas oito e o novo exame.']),
     ('labs-dark', ['Labs · dark mode', 'Labs · modo oscuro', 'Labs · modo escuro'], ['The same overview in dark mode, following the system setting.', 'El mismo resumen en modo oscuro, siguiendo el ajuste del sistema.', 'A mesma visão no modo escuro, seguindo o ajuste do sistema.']),
     ('launcher', ['Launcher', 'Inicio', 'Início'], ['The suite’s front door: pick Fuel or Labs.', 'La puerta de entrada: elige Fuel o Labs.', 'A porta de entrada: escolha Fuel ou Labs.'])]
S[4] = S[4] + (['Next week’s groceries by aisle with quantities, and the Friday Instacart cart that fills itself.', 'Las compras de la próxima semana por pasillo con cantidades, y el carrito de Instacart que se llena solo los viernes.', 'As compras da próxima semana por corredor com quantidades, e o carrinho do Instacart que se enche sozinho às sextas.'],)
S[8] = S[8] + (['Six systems with a range bar per marker: green band for the lab range, a tick for the athlete target, a hollow dot for the previous draw.', 'Seis sistemas con una barra por marcador: banda verde para el rango, una marca para la meta de atleta y un punto hueco para el análisis anterior.', 'Seis sistemas com uma barra por marcador: faixa verde para o laboratório, um traço para a meta de atleta e um ponto vazado para o exame anterior.'],)
SW = [('#0b1f3a', 'Navy #0b1f3a'), ('#1746a0', 'Deep #1746a0'), ('#2f6fec', 'Action #2f6fec'), ('#0ea5b7', 'Teal #0ea5b7'), ('#f59e0b', 'Carbs #f59e0b'), ('#7c5cff', 'Track #7c5cff'), ('#ef5b5b', 'Race #ef5b5b'), ('#f3f6fb', 'Ground #f3f6fb')]

e = lambda k: html.escape(C[k][0], quote=False)
thumbs = ''.join(f'<button class="th{" on" if i == 0 else ""}" data-i="{i}"><img src="{R}screens/{n}.jpg" alt="" loading="lazy"><span>{i + 1:02d}</span></button>' for i, (n, _, _) in enumerate(S))
how = ''.join(f'<div><span class="num">{i:02d}</span><h3 data-k="h{i}h">{e("h%dh" % i)}</h3><p data-k="h{i}">{e("h%d" % i)}</p></div>' for i in range(1, 7))
decisions = ''.join(f'<div><span class="num">{i:02d}</span><h3 data-k="d{i}h">{e("d%dh" % i)}</h3><p data-k="d{i}">{e("d%d" % i)}</p></div>' for i in range(1, 7))
sw = ''.join(f'<div><i style="background:{c}"></i><span>{n}</span></div>' for c, n in SW)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e('title')}</title>
<meta name="description" content="Fuel & Labs: a marathon nutrition planner and a lab results app built with Claude. Daily macros from the training plan, meals with recipes, Miami weather, a Friday Instacart cart, and seven blood panels in one view.">
<meta property="og:title" content="Fuel & Labs — Nutrition and lab results apps"><meta property="og:description" content="Daily fueling for every session of a 22-week marathon build, and three years of blood work in one clear view."><meta property="og:image" content="{R}social.jpg">
<link rel="canonical" href="https://www.wendelfreitas.com/fuel-and-labs/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--bg:#080808;--panel:#111;--line:#232323;--ink:#f4f4f1;--mute:#9a9a94;--lime:#c8f135;--blue:#2f6fec}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}button{{font:inherit;color:inherit;cursor:pointer}}.wrap{{max-width:1120px;margin:0 auto;padding:0 24px}}
:focus-visible{{outline:2px solid var(--lime);outline-offset:3px}}
header{{position:sticky;top:0;z-index:5;background:rgba(8,8,8,.86);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}}
header .wrap{{display:flex;align-items:center;gap:22px;min-height:64px}}
.logo{{font:800 22px Syne,sans-serif;text-decoration:none;letter-spacing:-.02em}}.logo span{{color:var(--lime)}}
nav{{display:flex;gap:22px;margin-left:auto;flex-wrap:wrap;align-items:center}}nav a{{font:500 12px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;color:var(--mute)}}nav a:hover,nav a[aria-current]{{color:var(--ink)}}
.cta{{background:var(--lime);color:#080808!important;padding:10px 16px;border-radius:6px;font:600 13px Inter,sans-serif!important;letter-spacing:0!important;text-transform:none!important}}
.eyebrow{{font:500 12px 'JetBrains Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--lime);margin:0 0 10px}}
h1{{font:800 clamp(44px,10vw,92px)/1 Syne,sans-serif;letter-spacing:-.03em;margin:14px 0 20px;text-wrap:balance}}h1 em{{font-style:normal;color:var(--lime)}}
h2{{font:700 clamp(26px,3.6vw,38px)/1.1 Syne,sans-serif;letter-spacing:-.02em;margin:0 0 18px;text-wrap:balance}}
.hero{{padding:72px 0 40px}}.lede{{max-width:700px;color:#c9c9c3;font-size:19px}}
.back{{font:500 12px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);text-decoration:none}}
.btns{{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}}.btn{{display:inline-block;padding:13px 20px;border-radius:6px;border:1px solid #3a3a3a;text-decoration:none;font-weight:600;font-size:15px;background:none}}.btn.p{{background:var(--lime);color:#080808;border-color:var(--lime)}}
.cover{{margin-top:44px;border-radius:14px;overflow:hidden;border:1px solid var(--line)}}.cover img{{display:block;width:100%;height:auto}}
.facts{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:24px 0 0}}
.facts div{{background:var(--panel);padding:22px}}.facts b{{display:block;font:800 34px Syne,sans-serif;color:var(--lime);letter-spacing:-.02em}}.facts span{{font:500 11px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}}
section{{padding:64px 0;border-top:1px solid var(--line)}}
.two{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:48px}}.two p{{margin:0 0 16px;color:#c9c9c3}}
.browser{{margin-top:28px;border-radius:14px;overflow:hidden;border:1px solid #2a3a56;background:#0b1f3a;box-shadow:0 40px 120px rgba(47,111,236,.22)}}
.bbar{{display:flex;align-items:center;gap:12px;padding:10px 14px;background:#0f1a2e;border-bottom:1px solid #22314a}}
.dots{{display:flex;gap:6px}}.dots i{{width:11px;height:11px;border-radius:50%;background:#ff5f57}}.dots i:nth-child(2){{background:#febc2e}}.dots i:nth-child(3){{background:#28c840}}
.tabs{{display:flex;gap:4px;background:#0b1424;border:1px solid #22314a;border-radius:999px;padding:3px}}
.tabs button{{border:0;background:none;border-radius:999px;padding:6px 16px;font:600 13px Inter,sans-serif;color:#93a3ba}}.tabs button.on{{background:#eef3fb;color:#0b1f3a}}
.url{{flex:1;max-width:420px;margin-left:auto;font:500 12px 'JetBrains Mono',monospace;color:#93a3ba;background:#0b1424;border-radius:8px;padding:6px 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.browser iframe{{display:block;width:100%;height:820px;border:0;background:#f3f6fb}}
.note{{font:500 11px 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin-top:16px}}
.mopen{{display:none;margin-top:20px;text-align:center;width:100%}}
.gal{{margin-top:28px}}.stage{{border-radius:12px;overflow:hidden;border:1px solid #2a2a2a;background:#0b1f3a}}.stage img{{display:block;width:100%;aspect-ratio:1440/900;object-fit:cover;object-position:top}}
.capw{{display:flex;gap:28px;align-items:flex-start;justify-content:space-between;margin:22px 0}}
.cap b{{font:800 28px Syne,sans-serif;display:block;letter-spacing:-.02em;margin-bottom:6px}}.cap p{{color:#c9c9c3;margin:0;max-width:640px;min-height:54px}}
.ctr{{font:500 12px 'JetBrains Mono',monospace;color:var(--lime);letter-spacing:.12em;display:block;margin-bottom:8px}}
.arrows{{display:flex;gap:8px;flex:none}}.arrows button{{width:44px;height:44px;border-radius:50%;border:1px solid #3a3a3a;background:none;font-size:18px}}.arrows button:hover{{border-color:var(--lime);color:var(--lime)}}
.thumbs{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}}
.th{{background:none;border:0;padding:0;text-align:left}}.th img{{width:100%;display:block;border-radius:8px;border:2px solid #222;aspect-ratio:16/10;object-fit:cover;object-position:top;transition:.15s;opacity:.6}}
.th span{{display:block;font:500 11px 'JetBrains Mono',monospace;letter-spacing:.08em;color:var(--mute);margin-top:6px}}
.th:hover img{{opacity:1}}.th.on img{{border-color:var(--lime);opacity:1}}.th.on span{{color:var(--ink)}}
.phones{{display:flex;gap:28px;justify-content:center;flex-wrap:wrap;margin-top:12px}}.phones img{{width:260px;height:auto;display:block;filter:drop-shadow(0 30px 60px rgba(47,111,236,.25))}}
.list{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-top:28px}}
.list div{{background:var(--panel);padding:24px}}.list h3{{font:700 18px Syne,sans-serif;margin:8px 0 6px}}.list p{{margin:0;color:var(--mute);font-size:15px}}.num{{font:500 12px 'JetBrains Mono',monospace;color:var(--lime)}}
.sw{{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}}.sw div{{width:112px}}.sw i{{display:block;height:56px;border-radius:8px;border:1px solid #2a2a2a}}.sw span{{font:500 11px 'JetBrains Mono',monospace;color:var(--mute);display:block;margin-top:6px}}
.tags{{display:flex;flex-wrap:wrap;gap:8px}}.tags span{{font:500 12px 'JetBrains Mono',monospace;border:1px solid #333;border-radius:999px;padding:7px 12px;color:#c9c9c3}}
footer{{border-top:1px solid var(--line);padding:36px 0 56px;color:var(--mute);font-size:14px}}footer .wrap{{display:flex;gap:18px;flex-wrap:wrap;justify-content:space-between}}
@media(max-width:979px){{.browser{{display:none}}.mopen{{display:block}}#full{{display:none}}.list{{grid-template-columns:1fr 1fr}}.thumbs{{grid-template-columns:repeat(4,minmax(0,1fr))}}}}
@media(max-width:820px){{.two{{grid-template-columns:1fr;gap:20px}}.facts{{grid-template-columns:repeat(2,minmax(0,1fr))}}.list{{grid-template-columns:1fr}}.hide-m{{display:none}}.hero{{padding:44px 0 28px}}section{{padding:44px 0}}.capw{{flex-direction:column;gap:12px}}.cap b{{font-size:22px}}.phones img{{width:46%}}}}
</style></head><body>
<header><div class="wrap"><a class="logo" href="/">W<span>F</span></a><nav><a class="hide-m" href="/">Home</a><a class="hide-m" href="/services">Services</a><a href="/cases" aria-current="page">Cases</a><a class="hide-m" href="/about">About</a><a class="cta" href="/contact">Get Free Audit →</a></nav></div></header>
<main>
<div class="wrap hero">
<a class="back" href="/cases" data-k="back">{e('back')}</a>
<p class="eyebrow" style="margin-top:28px" data-k="eyebrow">{e('eyebrow')}</p>
<h1>Fuel <em>&amp;</em> Labs</h1>
<p class="lede" data-k="lede">{e('lede')}</p>
<div class="btns"><a class="btn p" href="#try" data-k="b1">{e('b1')}</a><a class="btn" id="full" href="{APP}" target="_blank" rel="noopener" data-k="b2">{e('b2')}</a><a class="btn" href="https://github.com/wendel-crypto/fuel-and-labs" target="_blank" rel="noopener" data-k="b3">{e('b3')}</a></div>
<div class="cover"><img src="{R}cover.jpg" alt="Fuel and Labs on desktop and phone"></div>
<div class="facts"><div><b>154</b><span data-k="f1">{e('f1')}</span></div><div><b>31</b><span data-k="f2">{e('f2')}</span></div><div><b>42</b><span data-k="f3">{e('f3')}</span></div><div><b>2</b><span data-k="f4">{e('f4')}</span></div></div>
</div>
<section><div class="wrap two"><div><p class="eyebrow" data-k="pe">{e('pe')}</p><h2 data-k="ph">{e('ph')}</h2></div><div><p data-k="p1">{e('p1')}</p><p data-k="p2">{e('p2')}</p><p data-k="p3">{e('p3')}</p></div></div></section>
<section id="try"><div class="wrap">
<p class="eyebrow" data-k="te">{e('te')}</p><h2 data-k="th">{e('th')}</h2><p style="color:#c9c9c3;max-width:760px;margin:0" data-k="tp">{e('tp')}</p>
<div class="browser"><div class="bbar"><span class="dots"><i></i><i></i><i></i></span><span class="tabs"><button class="on" data-app="fuel" data-k="tf">Fuel</button><button data-app="labs" data-k="tl">Labs</button></span><span class="url" id="url">wendelfreitas.com/fuel-and-labs/app/fuel/</span></div><iframe id="app" title="Fuel and Labs live apps" loading="lazy"></iframe></div>
<a class="btn p mopen" href="{APP}" data-k="mopen">{e('mopen')}</a>
<p class="note" data-k="note">{e('note')}</p>
</div></section>
<section><div class="wrap">
<p class="eyebrow" data-k="se">{e('se')}</p><h2 data-k="sh">{e('sh')}</h2>
<div class="gal"><div class="stage"><img id="stageImg" src="{R}screens/{S[0][0]}.jpg" alt=""></div>
<div class="capw"><div class="cap"><span class="ctr" id="ctr">01 / {len(S):02d}</span><b id="capT">{html.escape(S[0][1][0])}</b><p id="capP">{html.escape(S[0][2][0])}</p></div><div class="arrows"><button id="prev" aria-label="Previous">←</button><button id="next" aria-label="Next">→</button></div></div>
<div class="thumbs">{thumbs}</div></div>
</div></section>
<section><div class="wrap two"><div><p class="eyebrow" data-k="me">{e('me')}</p><h2 data-k="mh">{e('mh')}</h2><p style="color:#c9c9c3" data-k="mp">{e('mp')}</p></div>
<div class="phones"><img src="{R}screens/fuel-mobile-frame.png" alt="Fuel on a phone"><img src="{R}screens/labs-mobile-frame.png" alt="Labs on a phone"></div></div></section>
<section><div class="wrap"><p class="eyebrow" data-k="he">{e('he')}</p><h2 data-k="hh">{e('hh')}</h2><div class="list">{how}</div></div></section>
<section><div class="wrap"><p class="eyebrow" data-k="de">{e('de')}</p><h2 data-k="dh">{e('dh')}</h2><div class="list">{decisions}</div></div></section>
<section><div class="wrap two"><div><p class="eyebrow" data-k="ye">{e('ye')}</p><h2 data-k="yh">{e('yh')}</h2></div><div><p data-k="y1">{e('y1')}</p><div class="sw">{sw}</div><p data-k="y2">{e('y2')}</p></div></div></section>
<section><div class="wrap two"><div><p class="eyebrow" data-k="re">{e('re')}</p><h2 data-k="rh">{e('rh')}</h2></div><div><p data-k="r1">{e('r1')}</p><p data-k="r2">{e('r2')}</p>
<div class="tags"><span>Product design</span><span>Data viz</span><span>Web apps</span><span>Claude</span><span>AI agents</span><span>Garmin</span><span>Instacart</span><span>Nutrition</span><span>Health</span></div></div></div></section>
</main>
<footer><div class="wrap"><span data-k="foot">{e('foot')}</span><span><a href="https://github.com/wendel-crypto/fuel-and-labs">GitHub</a> · <a href="/cases">Cases</a></span></div></footer>
<script>
const C={json.dumps(C, ensure_ascii=False)},S={json.dumps([[R + 'screens/' + n + '.jpg', t, p] for n, t, p in S], ensure_ascii=False)};
const APP='{APP}';
/* Language is owned by the shared site script (/wf-site.vN.js): it keeps 'wf-lang' and sets <html lang>. This page only follows it. */
const LI=()=>{{let l=document.documentElement.lang||'en';try{{if(!window.__wfSite)l=localStorage.getItem('wf-lang')||l}}catch(e){{}}l=l.slice(0,2);return l==='es'?1:l==='pt'?2:0}};
let li=LI(),cur=0;
const img=document.getElementById('stageImg'),T=document.getElementById('capT'),P=document.getElementById('capP'),N=document.getElementById('ctr'),th=[...document.querySelectorAll('.th')];
function show(i){{cur=(i+S.length)%S.length;img.src=S[cur][0];img.alt=S[cur][1][li];T.textContent=S[cur][1][li];P.textContent=S[cur][2][li];N.textContent=String(cur+1).padStart(2,'0')+' / '+String(S.length).padStart(2,'0');th.forEach((t,k)=>{{t.classList.toggle('on',k===cur);t.setAttribute('aria-label',S[k][1][li])}})}}
function applyLang(){{li=LI();document.title=C.title[li];document.querySelectorAll('[data-k]').forEach(n=>{{const v=C[n.dataset.k][li];if(n.textContent!==v)n.textContent=v}});show(cur)}}
const fr=document.getElementById('app'),url=document.getElementById('url'),desk=matchMedia('(min-width:980px)');
function load(a){{document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.app===a));fr.src=APP+a+'/?embed&date=2026-11-24';url.textContent='wendelfreitas.com'+APP+a+'/'}}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>load(b.dataset.app));
const io='IntersectionObserver' in window?new IntersectionObserver(e=>{{if(e.some(x=>x.isIntersecting)&&desk.matches&&!fr.getAttribute('src')){{load('fuel');io.disconnect()}}}},{{rootMargin:'600px'}}):null;io?io.observe(document.getElementById('try')):(desk.matches&&load('fuel'));
th.forEach(t=>t.onclick=()=>show(+t.dataset.i));document.getElementById('prev').onclick=()=>show(cur-1);document.getElementById('next').onclick=()=>show(cur+1);
document.addEventListener('keydown',e=>{{if(e.target.closest&&e.target.closest('input,select,textarea'))return;if(e.key==='ArrowRight')show(cur+1);if(e.key==='ArrowLeft')show(cur-1)}});
new MutationObserver(applyLang).observe(document.documentElement,{{attributes:true,attributeFilter:['lang']}});
S.forEach(s=>{{new Image().src=s[0]}});applyLang();
</script>
<script src="/wf-site.v13.js" defer></script>
</body></html>
'''
(root / 'site').mkdir(exist_ok=True)
(root / 'site' / 'case-page.html').write_text(page, encoding='utf-8')
print('site/case-page.html', len(page), 'bytes')

card = '''    <script>
      // wf-case-fuel-labs: adds the Fuel & Labs card to Cases > App; the case page is standalone HTML at /fuel-and-labs/
      (function () {
        var busy = false;
        function sync() {
          if (busy) return; busy = true;
          try {
            var card = document.getElementById('wf-fuel-labs-card');
            var src = document.querySelector('a[href="/cases/rundate-miami"]');
            if (!src) { if (card) card.remove(); return; }
            if (card && card.parentElement === src.parentElement) return;
            if (card) card.remove();
            card = src.cloneNode(true); card.id = 'wf-fuel-labs-card'; card.setAttribute('href', '/fuel-and-labs/');
            var media = card.children[0], body = card.children[1];
            if (media) { media.innerHTML = '<img src="https://raw.githubusercontent.com/wendel-crypto/fuel-and-labs/main/docs/thumb.webp" alt="Fuel and Labs app screens" style="width:100%;height:100%;object-fit:cover;display:block">'; }
            if (body) {
              var k = body.children;
              if (k[0]) k[0].textContent = 'Personal product \\u00b7 Web apps \\u00b7 Health + AI agents';
              if (k[1]) k[1].textContent = 'Fuel & Labs';
              if (k[2]) k[2].textContent = 'A marathon nutrition planner and a lab results app built with Claude: daily macros from the training plan, meals with recipes, Miami weather, a Friday Instacart cart, and seven blood panels in one clear view.';
              if (k[3] && k[3].children.length) { var tags = ['Web apps', 'Data viz', 'AI agents', 'Nutrition', 'Health']; var t0 = k[3].children[0]; k[3].innerHTML = ''; tags.forEach(function (t) { var n = t0.cloneNode(false); n.textContent = t; k[3].appendChild(n); }); }
            }
            src.parentElement.appendChild(card);
          } catch (e) {} finally { busy = false; }
        }
        function start() { new MutationObserver(sync).observe(document.body, { childList: true, subtree: true }); sync(); }
        if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
      })();
    </script>
'''
(root / 'site' / 'cases-app-card.snippet.html').write_text(card, encoding='utf-8')
print('snippet ok')
