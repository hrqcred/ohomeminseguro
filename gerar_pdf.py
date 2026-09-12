from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import textwrap

INK = HexColor('#080A0C')
SURFACE = HexColor('#0F1318')
CARD = HexColor('#12151A')
TEXT = HexColor('#E8E0D5')
MUTED = HexColor('#7A7468')
EMBER = HexColor('#7C1D1D')
EMBER_GLOW = HexColor('#A32626')
DARK_RED = HexColor('#3A1515')
LIGHT_TEXT = HexColor('#C4BAB0')
DIM_TEXT = HexColor('#9A9490')
SUBTLE = HexColor('#5A564E')
WHITE = HexColor('#F0E8E0')
GREEN_ACCENT = HexColor('#2A5A2A')
GREEN_LIGHT = HexColor('#4A8A4A')

W, H = A4

def draw_bg(c, color=INK):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_line(c, x1, y1, x2, y2, color=EMBER, width=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)

def draw_text(c, text, x, y, font='Helvetica', size=10, color=TEXT, align='left', max_width=None):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == 'center' and max_width:
        tw = c.stringWidth(text, font, size)
        x = x + (max_width - tw) / 2
    elif align == 'right' and max_width:
        tw = c.stringWidth(text, font, size)
        x = x + max_width - tw
    c.drawString(x, y, text)

def draw_wrapped_text(c, text, x, y, font='Helvetica', size=10, color=TEXT, max_width=450, leading=16):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = []
    for paragraph in text.split('\n'):
        if paragraph.strip() == '':
            lines.append('')
            continue
        words = paragraph.split()
        current_line = ''
        for word in words:
            test = current_line + ' ' + word if current_line else word
            if c.stringWidth(test, font, size) <= max_width:
                current_line = test
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

    cy = y
    for line in lines:
        if cy < 60:
            c.showPage()
            draw_bg(c)
            cy = H - 60
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, cy, line)
        cy -= leading
    return cy

def draw_ember_accent(c, x, y, height=40):
    c.setStrokeColor(EMBER_GLOW)
    c.setLineWidth(2)
    c.line(x, y, x, y - height)

def draw_card(c, x, y, w, h):
    c.setFillColor(CARD)
    c.setStrokeColor(HexColor('#1E2128'))
    c.setLineWidth(0.5)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.setStrokeColor(EMBER_GLOW)
    c.setLineWidth(2)
    c.line(x, y + h, x, y + h - min(h, 60))

def draw_circle_bullet(c, x, y, color=EMBER):
    c.setFillColor(color)
    c.circle(x, y + 3, 3, fill=1, stroke=0)

def draw_check(c, x, y):
    c.setStrokeColor(EMBER_GLOW)
    c.setFillColor(HexColor('#120606'))
    c.circle(x, y + 3, 7, fill=1, stroke=1)
    c.setStrokeColor(EMBER_GLOW)
    c.setLineWidth(1.5)
    c.line(x - 3, y + 3, x - 1, y + 1)
    c.line(x - 1, y + 1, x + 3, y + 5)


# ═══════════════════════════════════════════════════
# PAGE BUILDERS
# ═══════════════════════════════════════════════════

def build_cover(c):
    draw_bg(c, INK)

    # Vertical ember line
    draw_line(c, 40, H - 80, 40, H - 160, EMBER_GLOW, 1.5)

    # Top label
    draw_text(c, 'TREINAMENTO DIGITAL', 50, H - 100, 'Helvetica', 9, MUTED)

    # Title
    draw_text(c, 'O Homem', 50, H - 220, 'Helvetica-Bold', 48, TEXT)
    draw_text(c, 'Inseguro', 50, H - 275, 'Helvetica-Bold', 48, TEXT)

    # Ember line under title
    draw_line(c, 50, H - 295, 130, H - 295, EMBER, 2)

    # Subtitle
    draw_wrapped_text(c, 'Identifique seus padroes. Quebre o ciclo.\nConstrua confianca real.',
                      50, H - 330, 'Helvetica', 14, LIGHT_TEXT, leading=22)

    # Bottom info
    draw_line(c, 50, 120, W - 50, 120, HexColor('#1C1E22'), 0.5)
    draw_text(c, '7 modulos  |  Exercicios praticos  |  Acesso vitalicio', 50, 95, 'Helvetica', 10, MUTED)
    draw_text(c, 'www.ohomeminseguro.store', 50, 75, 'Helvetica', 9, SUBTLE)

    # Glow effect (red circle)
    c.setFillColor(Color(0.49, 0.11, 0.11, alpha=0.08))
    c.circle(W - 100, H / 2, 200, fill=1, stroke=0)

def build_intro(c):
    c.showPage()
    draw_bg(c)

    draw_text(c, 'ANTES DE COMECAR', 50, H - 70, 'Helvetica', 9, MUTED)
    draw_line(c, 50, H - 78, 160, H - 78, EMBER, 1)

    draw_text(c, 'Uma conversa honesta', 50, H - 120, 'Helvetica-Bold', 28, TEXT)

    y = draw_wrapped_text(c,
        'Se voce esta lendo isso, provavelmente ja tentou de tudo.',
        50, H - 170, 'Helvetica', 12, LIGHT_TEXT, max_width=460, leading=20)

    y = draw_wrapped_text(c,
        'Tentou "nao ligar". Tentou controlar. Tentou fingir que nao sentia aquilo. '
        'Ouviu conselhos como "confia nela", "para de ser inseguro", "isso e coisa da sua cabeca". '
        'E no fundo voce sabia que era da sua cabeca. Mas nao conseguia parar.',
        50, y - 16, 'Helvetica', 11, DIM_TEXT, max_width=460, leading=18)

    y = draw_wrapped_text(c,
        'Este treinamento nao e motivacional. Nao tem frase de efeito vazia. '
        'E um material construido para quem quer entender de verdade o que acontece '
        'dentro de si e, mais importante, o que fazer com isso.',
        50, y - 16, 'Helvetica', 11, DIM_TEXT, max_width=460, leading=18)

    y = draw_wrapped_text(c,
        'Sao 7 modulos. Cada um ataca um ponto especifico da inseguranca masculina. '
        'Com explicacoes diretas, exemplos reais e exercicios praticos que voce pode '
        'aplicar no mesmo dia.',
        50, y - 16, 'Helvetica', 11, DIM_TEXT, max_width=460, leading=18)

    # Card
    card_y = y - 40
    draw_card(c, 50, card_y - 100, W - 100, 100)
    draw_text(c, 'IMPORTANTE', 70, card_y - 30, 'Helvetica-Bold', 10, EMBER_GLOW)
    draw_wrapped_text(c,
        'Este material tem finalidade educacional. Nao substitui acompanhamento '
        'psicologico ou psiquiatrico. Se voce sente que precisa de ajuda profissional, '
        'procure um terapeuta. Isso nao e fraqueza. E inteligencia.',
        70, card_y - 50, 'Helvetica', 10, DIM_TEXT, max_width=400, leading=16)

def build_sumario(c):
    c.showPage()
    draw_bg(c)

    draw_text(c, 'SUMARIO', 50, H - 70, 'Helvetica', 9, MUTED)
    draw_line(c, 50, H - 78, 100, H - 78, EMBER, 1)

    draw_text(c, 'O caminho completo', 50, H - 120, 'Helvetica-Bold', 28, TEXT)

    modulos = [
        ('01', 'A origem da inseguranca', 'De onde vem esse medo que parece nao ter explicacao'),
        ('02', 'O jogo da comparacao', 'Por que voce se mede contra outros e sempre perde'),
        ('03', 'A armadilha da validacao', 'A dependencia silenciosa de ser aprovado'),
        ('04', 'Ciume: o monstro familiar', 'O mapa completo para desarmar o gatilho'),
        ('05', 'Comportamentos que afastam', 'O inventario honesto de tudo que voce faz achando que protege'),
        ('06', 'Confianca interna', 'Como construir seguranca que nao depende de ninguem'),
        ('07', 'Comunicacao madura', 'Falar sem acusar, ouvir sem se defender'),
    ]

    y = H - 180
    for num, nome, desc in modulos:
        draw_ember_accent(c, 50, y + 8, 30)
        draw_text(c, f'MODULO {num}', 62, y + 4, 'Helvetica', 9, EMBER_GLOW)
        draw_text(c, nome, 62, y - 14, 'Helvetica-Bold', 14, TEXT)
        draw_text(c, desc, 62, y - 32, 'Helvetica', 10, DIM_TEXT)

        if num != '07':
            draw_line(c, 62, y - 44, W - 60, y - 44, HexColor('#1C1E22'), 0.3)

        y -= 70

def build_ciclo_page(c):
    c.showPage()
    draw_bg(c)

    draw_text(c, 'O CICLO INVISIVEL', 50, H - 70, 'Helvetica', 9, MUTED)
    draw_line(c, 50, H - 78, 170, H - 78, EMBER, 1)

    draw_text(c, 'Antes dos modulos:', 50, H - 120, 'Helvetica-Bold', 24, TEXT)
    draw_text(c, 'entenda o padrao', 50, H - 148, 'Helvetica-Bold', 24, TEXT)

    y = draw_wrapped_text(c,
        'A inseguranca nao e um evento isolado. E um ciclo que se alimenta. '
        'Cada estagio leva ao proximo, e o ultimo leva de volta ao primeiro. '
        'Enquanto voce nao enxergar o padrao, vai continuar preso nele.',
        50, H - 190, 'Helvetica', 11, DIM_TEXT, max_width=460, leading=18)

    etapas = [
        ('01', 'Medo', 'Um gatilho dispara. Uma mensagem, um nome, um silencio.'),
        ('02', 'Pensamentos', '"E se...?", "por que ela...?" Cenarios que nunca terminam bem.'),
        ('03', 'Comparacao', 'Voce se mede contra outros. Reais ou imaginados.'),
        ('04', 'Validacao', 'Busca prova de que ainda e suficiente. O alivio dura pouco.'),
        ('05', 'Impulso', 'A tensao vira acao: perguntas, invasoes, cenas.'),
        ('06', 'Arrependimento', 'A clareza chega depois. O que foi dito nao pode ser desfeito.'),
        ('07', 'Mais inseguranca', 'O comportamento confirma o medo. O ciclo recomeca.'),
    ]

    y -= 20
    for num, nome, desc in etapas:
        if y < 80:
            c.showPage()
            draw_bg(c)
            y = H - 70
        draw_circle_bullet(c, 58, y)
        draw_text(c, num, 72, y, 'Helvetica', 9, EMBER_GLOW)
        draw_text(c, nome, 95, y, 'Helvetica-Bold', 11, TEXT)
        draw_text(c, desc, 95, y - 16, 'Helvetica', 10, DIM_TEXT)
        y -= 44

    # Loop indicator
    draw_text(c, '>>> O CICLO RECOMECA <<<', 95, y - 10, 'Helvetica-Bold', 10, EMBER_GLOW)


# ═══════════════════════════════════════════════════
# MODULE BUILDER
# ═══════════════════════════════════════════════════

def build_module_cover(c, num, title, subtitle):
    c.showPage()
    draw_bg(c, INK)

    # Big module number
    c.setFillColor(HexColor('#1A1D22'))
    c.setFont('Helvetica-Bold', 160)
    c.drawString(W - 200, H - 240, num)

    draw_text(c, f'MODULO {num}', 50, H - 180, 'Helvetica', 10, EMBER_GLOW)
    draw_line(c, 50, H - 190, 130, H - 190, EMBER, 2)

    draw_text(c, title, 50, H - 240, 'Helvetica-Bold', 32, TEXT)

    draw_wrapped_text(c, subtitle, 50, H - 280, 'Helvetica', 13, LIGHT_TEXT, max_width=400, leading=20)

def build_module_content(c, sections):
    for section in sections:
        c.showPage()
        draw_bg(c)

        section_type = section.get('type', 'text')

        if section_type == 'text':
            if 'eyebrow' in section:
                draw_text(c, section['eyebrow'].upper(), 50, H - 60, 'Helvetica', 9, MUTED)
                draw_line(c, 50, H - 68, 50 + len(section['eyebrow']) * 7, H - 68, EMBER, 1)

            if 'title' in section:
                ty = H - 100 if 'eyebrow' in section else H - 70
                draw_text(c, section['title'], 50, ty, 'Helvetica-Bold', 22, TEXT)
                y = ty - 35
            else:
                y = H - 70

            if 'body' in section:
                for block in section['body']:
                    if y < 80:
                        c.showPage()
                        draw_bg(c)
                        y = H - 60

                    if isinstance(block, str):
                        y = draw_wrapped_text(c, block, 50, y, 'Helvetica', 11, DIM_TEXT, max_width=460, leading=18)
                        y -= 12
                    elif isinstance(block, dict):
                        if block.get('style') == 'heading':
                            draw_text(c, block['text'], 50, y, 'Helvetica-Bold', 14, TEXT)
                            y -= 24
                        elif block.get('style') == 'quote':
                            draw_line(c, 55, y + 8, 55, y - 30, EMBER_GLOW, 2)
                            y = draw_wrapped_text(c, block['text'], 70, y, 'Helvetica-Oblique', 12, LIGHT_TEXT, max_width=430, leading=18)
                            y -= 16
                        elif block.get('style') == 'bullet':
                            for item in block['items']:
                                if y < 80:
                                    c.showPage()
                                    draw_bg(c)
                                    y = H - 60
                                draw_circle_bullet(c, 58, y)
                                y = draw_wrapped_text(c, item, 72, y, 'Helvetica', 11, DIM_TEXT, max_width=440, leading=18)
                                y -= 8
                            y -= 8
                        elif block.get('style') == 'check':
                            for item in block['items']:
                                if y < 80:
                                    c.showPage()
                                    draw_bg(c)
                                    y = H - 60
                                draw_check(c, 62, y - 2)
                                y = draw_wrapped_text(c, item, 80, y, 'Helvetica', 11, DIM_TEXT, max_width=430, leading=18)
                                y -= 8
                            y -= 8
                        elif block.get('style') == 'card':
                            card_h = block.get('height', 80)
                            if y - card_h < 60:
                                c.showPage()
                                draw_bg(c)
                                y = H - 60
                            draw_card(c, 50, y - card_h, W - 100, card_h)
                            if 'label' in block:
                                draw_text(c, block['label'], 70, y - 20, 'Helvetica-Bold', 10, EMBER_GLOW)
                            draw_wrapped_text(c, block['text'], 70, y - 38, 'Helvetica', 10, DIM_TEXT, max_width=400, leading=16)
                            y -= card_h + 16
                        elif block.get('style') == 'exercise_header':
                            draw_line(c, 50, y + 4, W - 50, y + 4, EMBER, 0.5)
                            y -= 10
                            draw_text(c, 'EXERCICIO PRATICO', 50, y, 'Helvetica-Bold', 11, EMBER_GLOW)
                            y -= 22
                        elif block.get('style') == 'numbered':
                            for i, item in enumerate(block['items'], 1):
                                if y < 80:
                                    c.showPage()
                                    draw_bg(c)
                                    y = H - 60
                                draw_text(c, f'{i:02d}', 55, y, 'Helvetica', 9, EMBER_GLOW)
                                y = draw_wrapped_text(c, item, 80, y, 'Helvetica', 11, DIM_TEXT, max_width=430, leading=18)
                                y -= 10
                            y -= 6
                        elif block.get('style') == 'transformation':
                            if y - 60 < 60:
                                c.showPage()
                                draw_bg(c)
                                y = H - 60
                            # Before
                            c.setFillColor(HexColor('#5A2020'))
                            c.setFont('Helvetica', 8)
                            c.drawString(55, y, 'ANTES')
                            draw_text(c, block['before'], 55, y - 16, 'Helvetica', 11, HexColor('#6A5A58'))
                            # Arrow
                            draw_text(c, '>>>', W/2 - 15, y - 8, 'Helvetica-Bold', 12, EMBER_GLOW)
                            # After
                            c.setFillColor(GREEN_ACCENT)
                            c.setFont('Helvetica', 8)
                            c.drawString(W/2 + 30, y, 'DEPOIS')
                            draw_text(c, block['after'], W/2 + 30, y - 16, 'Helvetica', 11, GREEN_LIGHT)
                            y -= 44


# ═══════════════════════════════════════════════════
# MODULE CONTENT DATA
# ═══════════════════════════════════════════════════

def get_module_01():
    return [
        {
            'eyebrow': 'Modulo 01',
            'title': 'De onde vem tudo isso?',
            'body': [
                'A inseguranca que voce sente hoje nao nasceu no seu relacionamento atual. '
                'Ela e mais antiga. Vem de antes. De lugares que voce talvez nem lembre.',
                'Para mudar alguma coisa, voce precisa primeiro entender como ela comecou. '
                'Nao como desculpa, mas como mapa. Saber de onde vem te ajuda a parar de repetir.',
                {'style': 'heading', 'text': 'As raizes da inseguranca masculina'},
                'Existem tres grandes fontes de inseguranca que a maioria dos homens carrega:',
                {'style': 'bullet', 'items': [
                    'Experiencias da infancia: a forma como voce foi criado, as mensagens que recebeu sobre o que significa "ser homem", a presenca ou ausencia de figuras de referencia.',
                    'Experiencias relacionais: traicoes, abandonos, rejeicoes. Situacoes que ensinaram seu cerebro que amar e perigoso.',
                    'Narrativa interna: a historia que voce conta sobre si mesmo. "Eu nao sou suficiente", "alguem melhor sempre vai aparecer", "eu nao mereco isso".',
                ]},
                'A maioria dos homens nunca para para olhar essas raizes. Eles tentam resolver o sintoma '
                '(o ciume, o controle, a inseguranca) sem entender a causa. E como tomar remedio para febre '
                'sem tratar a infeccao.',
            ]
        },
        {
            'title': 'O cerebro inseguro',
            'body': [
                'Quando voce sente aquele aperto no peito ao ver ela conversando com outro cara, '
                'nao e "frescura". Seu cerebro esta ativando o mesmo circuito de ameaca que nossos '
                'ancestrais usavam para sobreviver.',
                'A amigdala cerebral interpreta a situacao como perigo real. O cortisol sobe. '
                'A frequencia cardiaca aumenta. Voce entra em modo de luta ou fuga.',
                {'style': 'quote', 'text': 'O problema nao e sentir. O problema e reagir ao sentimento como se ele fosse um fato.'},
                'Seu cerebro nao distingue entre uma ameaca real (ela esta te traindo) e uma ameaca '
                'imaginada (ela sorriu para o garcom). A resposta fisiologica e a mesma.',
                {'style': 'heading', 'text': 'O modelo mental que voce herdou'},
                'A sociedade ensina ao homem que:',
                {'style': 'bullet', 'items': [
                    'Valor masculino = conquista. Se voce nao "conquista" e "mantem", nao e homem o suficiente.',
                    'Vulnerabilidade = fraqueza. Sentir medo de perder e "coisa de mulher". Homem "de verdade" nao sente isso.',
                    'Controle = protecao. Se voce controla a situacao, voce esta seguro. Perder o controle e perder tudo.',
                ]},
                'Essas crencas criam uma armadilha perfeita: voce sente inseguranca (normal), '
                'mas acredita que nao deveria sentir (vergonha), entao tenta controlar o ambiente '
                'externo (comportamento destrutivo) em vez de regular o ambiente interno (autoconsciencia).',
            ]
        },
        {
            'title': 'Exercicio: Mapeando suas raizes',
            'body': [
                {'style': 'exercise_header'},
                'Este exercicio e para voce fazer com honestidade, sem julgamento. Nao existe resposta certa ou errada. '
                'O objetivo e olhar para o que esta por tras do que voce sente.',
                {'style': 'heading', 'text': 'Parte 1: Inventario de origem'},
                'Responda por escrito (papel ou celular, o que preferir):',
                {'style': 'numbered', 'items': [
                    'Qual e a sua primeira memoria de sentir que "nao era suficiente"? O que aconteceu? Quantos anos voce tinha?',
                    'Quando crianca, voce recebia elogios com frequencia? Ou o padrao era mais de critica, silencio ou indiferenca?',
                    'Seu pai (ou figura paterna) demonstrava afeto abertamente? Como ele lidava com inseguranca?',
                    'Voce ja foi traido, abandonado ou rejeitado de forma significativa? O que isso te "ensinou" sobre relacionamentos?',
                    'Complete a frase: "No fundo, eu acredito que nao sou suficiente porque ___".',
                ]},
                {'style': 'heading', 'text': 'Parte 2: Reconhecimento'},
                'Releia suas respostas. Agora, observe:',
                {'style': 'bullet', 'items': [
                    'Quantas dessas crencas voce formou ANTES dos 15 anos?',
                    'Quantas vieram de situacoes que voce nao controlava?',
                    'Quantas voce nunca questionou ate agora?',
                ]},
                {'style': 'card', 'height': 60, 'label': 'REFLEXAO',
                 'text': 'Se a maioria das suas insegurancas nasceu antes de voce ter maturidade para questiona-las, faz sentido que elas ainda te controlem. Mas agora voce tem a maturidade. E esse e o primeiro passo.'},
            ]
        },
    ]

def get_module_02():
    return [
        {
            'eyebrow': 'Modulo 02',
            'title': 'O radar que nunca desliga',
            'body': [
                'Voce entra num restaurante com ela. Automaticamente, seus olhos escaneiam o ambiente. '
                'Quem olhou para ela? Tem alguem mais atraente aqui? Ela notou aquele cara?',
                'Isso nao e ciume. E comparacao. E um programa que roda em segundo plano na sua mente, '
                '24 horas por dia, medindo voce contra outros homens.',
                {'style': 'quote', 'text': 'Voce nao perde a batalha da comparacao porque o outro e melhor. Voce perde porque esta jogando um jogo que nao pode ser vencido.'},
                {'style': 'heading', 'text': 'Por que voce sempre perde'},
                'A comparacao e um sistema viciado porque:',
                {'style': 'bullet', 'items': [
                    'Voce compara o seu interior com o exterior do outro. Voce conhece todas as suas falhas, '
                    'insegurancas e defeitos. Do outro, voce so ve a fachada.',
                    'O alvo muda constantemente. Hoje e o colega de trabalho dela, amanha e o ex, depois e um '
                    'desconhecido no Instagram. O rival nao e real. E qualquer um.',
                    'A comparacao confirma o que voce ja acredita. Se voce acha que nao e suficiente, '
                    'vai encontrar evidencias disso em qualquer lugar.',
                ]},
            ]
        },
        {
            'title': 'O rival imaginario',
            'body': [
                'Existe uma verdade que a maioria dos homens inseguros nao quer ouvir:',
                {'style': 'quote', 'text': 'O rival quase nunca e outro homem. E uma versao idealizada que voce criou na sua cabeca. Um fantasma que nao erra, nao duvida, nao sente medo. E exatamente por isso que ele nao existe.'},
                'Voce nao esta competindo com o ex dela, com o colega de trabalho, com o cara da academia. '
                'Voce esta competindo com uma projecao do que voce acredita que deveria ser.',
                {'style': 'heading', 'text': 'Como a comparacao funciona no cerebro'},
                'O cerebro humano foi feito para comparar. Na era primitiva, isso era util: '
                'quem e mais forte? Quem e mais rapido? Quem e mais apto para sobreviver?',
                'O problema e que hoje voce usa o mesmo mecanismo para comparar coisas subjetivas: '
                'quem e mais "interessante", mais "confiante", mais "atraente". E essas comparacoes '
                'nao tem resposta objetiva. Entao sua mente inventa uma. E a resposta que ela inventa '
                'e sempre: "voce e menos".',
                {'style': 'heading', 'text': 'O efeito cascata'},
                {'style': 'numbered', 'items': [
                    'Voce ve um cara que parece confiante perto dela.',
                    'Sua mente automaticamente assume que ele e "mais" que voce.',
                    'Voce sente desconforto, ansiedade, irritacao.',
                    'Esse sentimento reforça a crenca de que voce nao e suficiente.',
                    'Na proxima vez, a comparacao e ainda mais rapida e intensa.',
                ]},
            ]
        },
        {
            'title': 'Exercicio: Desligando o radar',
            'body': [
                {'style': 'exercise_header'},
                {'style': 'heading', 'text': 'Parte 1: O diario da comparacao'},
                'Durante os proximos 3 dias, toda vez que voce se pegar comparando, anote:',
                {'style': 'numbered', 'items': [
                    'Com quem voce se comparou?',
                    'O que exatamente voce achou que o outro tinha e voce nao?',
                    'Voce estava comparando fatos ou suposicoes?',
                    'Essa comparacao te ajudou em alguma coisa?',
                ]},
                {'style': 'heading', 'text': 'Parte 2: A tecnica do zoom out'},
                'Quando o radar ligar, faca isso:',
                {'style': 'numbered', 'items': [
                    'PARE. Reconheca que o radar ligou. Nao julgue, apenas note.',
                    'PERGUNTE: "Eu sei TUDO sobre essa pessoa? Ou so estou vendo a superficie?"',
                    'RELEMBRE: "Comparacao e um jogo que nao pode ser vencido. Eu nao preciso jogar."',
                    'REDIRECIONE: Volte a atencao para voce. Nao para se julgar, mas para se ancorar no que voce E, nao no que o outro PARECE ser.',
                ]},
                {'style': 'card', 'height': 50, 'label': 'LEMBRETE',
                 'text': 'Comparacao e um habito. Habitos nao somem do dia para a noite. Eles sao substituidos. Cada vez que voce pratica o zoom out, esta treinando um novo padrao.'},
            ]
        },
    ]

def get_module_03():
    return [
        {
            'eyebrow': 'Modulo 03',
            'title': 'O poco sem fundo',
            'body': [
                'Voce precisa ouvir que e amado. Que e escolhido. Que nao vai ser trocado. '
                'Ela diz. Voce sente alivio. Por cinco minutos. Depois a duvida volta.',
                {'style': 'quote', 'text': 'A validacao externa e como beber agua salgada. Quanto mais voce bebe, mais sede sente.'},
                'A busca por validacao e uma das armadilhas mais silenciosas da inseguranca. '
                'Voce nem percebe que esta fazendo. Parece normal. Parece amor. Mas e dependencia.',
                {'style': 'heading', 'text': 'Sinais de que voce e dependente de validacao'},
                {'style': 'check', 'items': [
                    'Voce checa se ela visualizou sua mensagem e calcula o tempo de resposta.',
                    'Quando ela elogia outro homem (um ator, um cantor), voce se sente ameacado.',
                    'Voce pede confirmacao indireta: "Voce ainda me acha bonito?", "Voce nao preferia estar com outro?"',
                    'O humor do seu dia depende de como ela te trata naquele momento.',
                    'Voce se sente em paz so quando tem "prova" de que tudo esta bem.',
                ]},
                'Se marcou 3 ou mais, a validacao esta controlando suas emocoes. '
                'Nao e sobre ser carente. E sobre ter construido sua autoestima sobre uma base que nao e sua.',
            ]
        },
        {
            'title': 'O mecanismo da dependencia',
            'body': [
                {'style': 'heading', 'text': 'Por que nenhuma validacao e suficiente'},
                'O ciclo da validacao funciona assim:',
                {'style': 'numbered', 'items': [
                    'Voce sente inseguranca (gatilho interno).',
                    'Busca uma confirmacao externa (pergunta, teste, cobranca).',
                    'Recebe a validacao (ela responde, elogia, garante).',
                    'Sente alivio temporario (o cortisol baixa, a ansiedade diminui).',
                    'O alivio acaba (porque a causa raiz nao foi tratada).',
                    'A inseguranca volta, mais forte (porque agora voce "precisa" de mais validacao para o mesmo efeito).',
                ]},
                'E o mesmo mecanismo de qualquer dependencia. Tolerancia crescente. '
                'O que funcionava ontem nao funciona hoje. Voce precisa de mais.',
                {'style': 'heading', 'text': 'A pergunta que voce precisa se fazer'},
                {'style': 'quote', 'text': '"Se ela dissesse agora que me ama, eu acreditaria de verdade? Ou precisaria ouvir de novo amanha?"'},
                'Se a resposta e "precisaria ouvir de novo", o problema nao e a falta de validacao. '
                'E a incapacidade de recebe-la. Porque voce nao acredita, no fundo, que merece.',
            ]
        },
        {
            'title': 'Exercicio: Construindo base propria',
            'body': [
                {'style': 'exercise_header'},
                {'style': 'heading', 'text': 'Parte 1: O inventario de valor'},
                'Escreva, sem modestia e sem censura:',
                {'style': 'numbered', 'items': [
                    '5 coisas que voce faz bem (nao precisa ser excepcional, apenas honesto).',
                    '3 momentos em que voce foi forte quando poderia ter desistido.',
                    '2 pessoas que confiam em voce e por que.',
                    '1 qualidade sua que voce sabe que e real, nao importa o que ninguem diga.',
                ]},
                {'style': 'heading', 'text': 'Parte 2: O teste de 24 horas'},
                'Nas proximas 24 horas, faca um experimento:',
                {'style': 'bullet', 'items': [
                    'Nao peca validacao a ela. Nenhuma. Zero.',
                    'Nao cheque se ela viu sua mensagem.',
                    'Nao faca perguntas que so servem para confirmar que ela te quer.',
                    'Quando a ansiedade subir, anote o que voce esta sentindo e o que gostaria de perguntar.',
                ]},
                'No final das 24 horas, releia suas anotacoes. Observe quantas vezes voce quis buscar '
                'confirmacao. Observe que, mesmo sem buscar, nada de ruim aconteceu.',
                {'style': 'card', 'height': 60, 'label': 'VERDADE DURA',
                 'text': 'Voce nao precisa que ela te valide para estar bem. Voce QUER que ela te valide porque nunca aprendeu a se validar sozinho. Esse modulo existe para mudar isso.'},
            ]
        },
    ]

def get_module_04():
    return [
        {
            'eyebrow': 'Modulo 04',
            'title': 'O que e o ciume de verdade',
            'body': [
                'Ciume nao e amor. Ciume nao e cuidado. Ciume nao e sinal de que voce se importa.',
                'Ciume e medo. Medo de perder. Medo de ser substituido. Medo de nao ser suficiente. '
                'E uma resposta emocional primitiva que nao protege nada. Ela so destrói.',
                {'style': 'quote', 'text': 'O ciume nao protege o relacionamento. Ele protege a sua ilusao de controle. E quando a ilusao cai, o relacionamento ja foi embora.'},
                {'style': 'heading', 'text': 'Os tres tipos de ciume'},
                {'style': 'numbered', 'items': [
                    'Ciume reativo: resposta a uma ameaca real e concreta (traicao confirmada, mentira descoberta). Este e o unico que tem base na realidade.',
                    'Ciume ansioso: resposta a uma ameaca imaginada. Nao existe evidencia, mas o medo e real. E o tipo mais comum nos homens inseguros.',
                    'Ciume possessivo: nao e sobre medo de perder. E sobre controle. A outra pessoa e tratada como propriedade. Este e o mais destrutivo.',
                ]},
                'A maioria dos homens inseguros vive entre o ciume ansioso e o possessivo. '
                'Eles sentem medo sem motivo real e reagem tentando controlar a situacao.',
            ]
        },
        {
            'title': 'Anatomia de uma crise de ciume',
            'body': [
                'Vamos dissecar o que acontece no seu corpo e mente durante uma crise:',
                {'style': 'heading', 'text': 'Fase 1: O gatilho (0 a 3 segundos)'},
                'Algo acontece: ela demora para responder, menciona um nome, ri de uma piada de outro cara. '
                'Seu cerebro registra isso como PERIGO. A amigdala dispara.',
                {'style': 'heading', 'text': 'Fase 2: A inundacao (3 a 30 segundos)'},
                'O cortisol e a adrenalina inundam seu corpo. Seu coracao acelera. Suas maos suam. '
                'Seu estomago aperta. Voce nao esta pensando racionalmente. Voce esta em modo de sobrevivencia.',
                {'style': 'heading', 'text': 'Fase 3: A narrativa (30 segundos a 5 minutos)'},
                'Sua mente cria uma historia para justificar o que o corpo esta sentindo. '
                '"Ela esta escondendo algo." "Aquele cara esta dando em cima dela." "Ela vai me trocar." '
                'A historia parece logica porque o corpo ja decidiu que e verdade.',
                {'style': 'heading', 'text': 'Fase 4: A acao (5 a 30 minutos)'},
                'Voce age com base na historia, nao nos fatos. Faz uma pergunta que parece casual mas e um interrogatorio. '
                'Checa o celular. Manda mensagens testando. Faz uma "cena". O dano ja esta feito.',
                {'style': 'heading', 'text': 'A janela de oportunidade'},
                {'style': 'card', 'height': 70, 'label': 'CHAVE DO MODULO',
                 'text': 'Entre a Fase 2 e a Fase 3, existe uma janela. Um espaco de segundos onde voce AINDA PODE ESCOLHER. O ciume ja foi sentido, mas a historia ainda nao foi construida. E nessa janela que voce precisa aprender a agir.'},
            ]
        },
        {
            'title': 'Exercicio: O protocolo de 90 segundos',
            'body': [
                {'style': 'exercise_header'},
                'Neurocientistas descobriram que uma emocao leva cerca de 90 segundos para percorrer '
                'o corpo e se dissipar. Se voce conseguir nao agir durante esses 90 segundos, '
                'a intensidade cai drasticamente.',
                {'style': 'heading', 'text': 'O Protocolo:'},
                {'style': 'numbered', 'items': [
                    'RECONHECA: Diga para si mesmo (mentalmente): "Estou sentindo ciume agora. E uma emocao. Nao e um fato."',
                    'RESPIRE: 4 segundos inspirando. 7 segundos segurando. 8 segundos expirando. Repita 3 vezes.',
                    'ANCORE: Sinta seus pes no chao. Suas maos. A temperatura do ar. Traga-se para o presente.',
                    'QUESTIONE: "Eu tenho evidencia concreta de que algo esta errado? Ou estou reagindo a uma historia que minha mente criou?"',
                    'DECIDA: "O que eu faria agora se estivesse seguro?" Faca isso.',
                ]},
                {'style': 'heading', 'text': 'Quando praticar'},
                {'style': 'bullet', 'items': [
                    'Toda vez que sentir o gatilho do ciume disparar.',
                    'Antes de mandar qualquer mensagem quando estiver ansioso.',
                    'Antes de fazer qualquer pergunta que so serve para testar ela.',
                    'Antes de checar o celular, o Instagram, ou qualquer fonte de "informacao".',
                ]},
                'Nos primeiros dias, voce pode nao conseguir completar o protocolo antes de reagir. '
                'Tudo bem. O objetivo nao e perfeicao. E progresso. Se na primeira semana voce conseguir '
                'parar 2 de cada 10 vezes, ja esta treinando um novo padrao.',
            ]
        },
    ]

def get_module_05():
    return [
        {
            'eyebrow': 'Modulo 05',
            'title': 'O inventario da destruicao',
            'body': [
                'Este e o modulo mais desconfortavel. Porque aqui voce vai olhar para o que VOCE faz. '
                'Nao o que ela faz. Nao o que os outros fazem. O que VOCE faz.',
                'A maioria dos comportamentos destrutivos parece "normal" quando voce esta no meio deles. '
                'Parece protecao. Parece cuidado. Parece amor.',
                {'style': 'quote', 'text': 'Controle nao e amor. E medo disfarçado de cuidado.'},
                {'style': 'heading', 'text': 'Comportamentos que parecem "normais" mas destroem'},
                {'style': 'numbered', 'items': [
                    'Checar o celular dela. Mesmo "so uma olhadinha". Mesmo quando ela sabe.',
                    'Interrogar sobre onde esteve, com quem falou, por que demorou.',
                    'Seguir perfis nas redes sociais para "monitorar" interacoes.',
                    'Fazer perguntas capciosas para ver se ela "cai" em contradicoes.',
                    'Fazer cenas em publico quando outro homem se aproxima.',
                    'Dar tratamento de silencio como punicao quando ela faz algo que voce nao aprova.',
                    'Comparar ela com outras mulheres para "testar" a reacao.',
                    'Exigir transparencia total enquanto esconde os proprios comportamentos.',
                    'Usar o passado dela contra ela em discussoes.',
                    'Ameacar terminar como forma de manipulacao.',
                ]},
                'Se voce faz 3 ou mais desses, nao e um sinal de que voce e uma pessoa ruim. '
                'E um sinal de que a inseguranca esta no controle. E que voce precisa retomar o volante.',
            ]
        },
        {
            'title': 'O custo real',
            'body': [
                {'style': 'heading', 'text': 'O que voce perde enquanto tenta "proteger"'},
                {'style': 'transformation', 'before': 'Voce quer seguranca', 'after': 'Ela se sente presa'},
                {'style': 'transformation', 'before': 'Voce quer proximidade', 'after': 'Ela se afasta'},
                {'style': 'transformation', 'before': 'Voce quer prova de amor', 'after': 'Ela se cansa de provar'},
                {'style': 'transformation', 'before': 'Voce quer controle', 'after': 'Ela perde respeito'},
                {'style': 'transformation', 'before': 'Voce quer que ela fique', 'after': 'Voce a empurra para ir'},
                '',
                'Cada comportamento de controle cria exatamente o resultado que voce mais teme. '
                'Voce age para nao perder e, com cada acao, perde mais.',
                {'style': 'heading', 'text': 'A espiral do desgaste'},
                'Relacionamentos nao terminam por causa de uma unica cena. Eles terminam por acumulo. '
                'Cada interrogatorio, cada desconfianca, cada invasao de privacidade deposita uma pedra '
                'no saco que ela carrega. Um dia, o saco fica pesado demais.',
                {'style': 'card', 'height': 50, 'label': 'VERDADE DIFICIL',
                 'text': 'Se voce perdeu um relacionamento por inseguranca, nao foi por um unico erro. Foi por um padrao que voce nao soube quebrar a tempo. Esse modulo existe para que o proximo nao termine igual.'},
            ]
        },
        {
            'title': 'Exercicio: O inventario honesto',
            'body': [
                {'style': 'exercise_header'},
                {'style': 'heading', 'text': 'Parte 1: Lista de comportamentos'},
                'Revise a lista dos 10 comportamentos destrutivos. Para cada um que voce pratica, escreva:',
                {'style': 'numbered', 'items': [
                    'Quando foi a ultima vez que fiz isso?',
                    'O que eu senti ANTES de fazer?',
                    'O que eu esperava conseguir com isso?',
                    'O que realmente aconteceu depois?',
                ]},
                {'style': 'heading', 'text': 'Parte 2: A substituicao'},
                'Para cada comportamento identificado, defina uma alternativa:',
                {'style': 'bullet', 'items': [
                    'Em vez de checar o celular dela > escrever no diario o que estou sentindo.',
                    'Em vez de interrogar > perguntar "como foi seu dia?" com interesse genuino.',
                    'Em vez de silencio punitivo > dizer "preciso de um tempo para organizar o que sinto".',
                    'Em vez de cena em publico > respirar e conversar em particular depois.',
                ]},
                'A substituicao nao e sobre engolir o que sente. E sobre expressar de forma diferente.',
            ]
        },
    ]

def get_module_06():
    return [
        {
            'eyebrow': 'Modulo 06',
            'title': 'O pilar que faltava',
            'body': [
                'Ate agora, voce entendeu de onde vem a inseguranca, como ela funciona e o que ela te faz fazer. '
                'Agora vem a parte construtiva: o que colocar no lugar.',
                {'style': 'quote', 'text': 'Confianca nao e a ausencia de medo. E a capacidade de agir bem apesar dele.'},
                'A confianca que voce precisa nao vem de fora. Nao vem de ela te provar que te ama. '
                'Nao vem de ser melhor que outros homens. Nao vem de ter controle sobre a situacao.',
                'Ela vem de dentro. De saber quem voce e, o que voce vale e o que voce escolhe fazer '
                'com o que sente.',
                {'style': 'heading', 'text': 'Os 4 pilares da confianca interna'},
                {'style': 'numbered', 'items': [
                    'Autoconhecimento: Saber o que te dispara, o que te faz reagir, quais sao seus padroes. Voce ja esta construindo isso desde o Modulo 01.',
                    'Autorregulacao: A capacidade de sentir a emocao sem ser controlado por ela. Reconhecer, processar, escolher. E o que o Protocolo de 90 Segundos treina.',
                    'Autovalor: Saber o que voce traz para a mesa. Nao por arrogancia, mas por honestidade. Reconhecer que voce tem valor independente de validacao externa.',
                    'Autossuficiencia emocional: Nao depender de uma unica pessoa para sua estabilidade. Ter uma base interna que nao desmorona quando o externo balanca.',
                ]},
            ]
        },
        {
            'title': 'Construindo cada pilar',
            'body': [
                {'style': 'heading', 'text': 'Pilar 1: Autoconhecimento diario'},
                'Reserve 5 minutos por dia (de preferencia no final do dia) para responder:',
                {'style': 'bullet', 'items': [
                    'O que eu senti hoje que me tirou do eixo?',
                    'O que disparou esse sentimento?',
                    'Como eu reagi?',
                    'Como eu gostaria de ter reagido?',
                ]},
                'Com o tempo, voce começa a ver padroes. E quando ve padroes, pode antecipa-los.',
                {'style': 'heading', 'text': 'Pilar 2: Pratica de autorregulacao'},
                'Alem do Protocolo de 90 Segundos, incorpore:',
                {'style': 'bullet', 'items': [
                    'Atividade fisica regular (qualquer uma). O corpo precisa descarregar a tensao acumulada.',
                    'Momentos de silencio. Sem celular, sem estimulo. Aprender a estar consigo mesmo sem desconforto.',
                    'Nomear emocoes. Nao "estou mal". Mas "estou sentindo ciume porque ela demorou para responder e meu cerebro criou uma historia".',
                ]},
                {'style': 'heading', 'text': 'Pilar 3: Reconstruindo autovalor'},
                'O autovalor nao se constroi com afirmacoes positivas no espelho. Se constroi com evidencias:',
                {'style': 'bullet', 'items': [
                    'Cumpra pequenas promessas que faz a si mesmo. Disse que ia acordar cedo? Acorde.',
                    'Invista em algo que e so seu: um hobby, um estudo, um projeto.',
                    'Pare de se depreciar, mesmo como "piada". Seu cerebro nao entende ironia.',
                ]},
                {'style': 'heading', 'text': 'Pilar 4: Autossuficiencia emocional'},
                {'style': 'card', 'height': 70, 'label': 'PRINCIPIO CENTRAL',
                 'text': 'Voce nao precisa que ela seja sua unica fonte de seguranca emocional. Tenha amigos, tenha proposito, tenha uma vida que faz sentido mesmo quando o relacionamento tem um dia ruim. Isso nao e "nao se importar". E nao se destruir.'},
            ]
        },
        {
            'title': 'Exercicio: O plano de 30 dias',
            'body': [
                {'style': 'exercise_header'},
                'Este e o exercicio mais importante do treinamento. E um compromisso de 30 dias com voce mesmo.',
                {'style': 'heading', 'text': 'Semana 1: Observacao'},
                {'style': 'bullet', 'items': [
                    'Faca o diario de 5 minutos todos os dias.',
                    'Nao tente mudar nada. Apenas observe e registre.',
                    'Identifique seus 3 gatilhos mais frequentes.',
                ]},
                {'style': 'heading', 'text': 'Semana 2: Interrupcao'},
                {'style': 'bullet', 'items': [
                    'Use o Protocolo de 90 Segundos sempre que um gatilho disparar.',
                    'Antes de qualquer comportamento reativo, conte ate 10.',
                    'Meta: interromper pelo menos 3 reacoes automaticas na semana.',
                ]},
                {'style': 'heading', 'text': 'Semana 3: Substituicao'},
                {'style': 'bullet', 'items': [
                    'Substitua 1 comportamento destrutivo pela alternativa saudavel.',
                    'Comece uma atividade que e so sua (esporte, leitura, projeto).',
                    'Pratique uma conversa honesta com ela sem acusar ou cobrar.',
                ]},
                {'style': 'heading', 'text': 'Semana 4: Consolidacao'},
                {'style': 'bullet', 'items': [
                    'Revise seu diario. Compare o dia 1 com o dia 28.',
                    'Identifique o que mudou na forma como voce reage.',
                    'Celebre o progresso. Sem exagero, sem diminuir.',
                ]},
            ]
        },
    ]

def get_module_07():
    return [
        {
            'eyebrow': 'Modulo 07',
            'title': 'Falar sem destruir',
            'body': [
                'A maioria dos conflitos em relacionamentos nao acontece por causa do PROBLEMA. '
                'Acontece por causa de COMO o problema e comunicado.',
                'Homens inseguros tendem a dois extremos: explodem ou engolem. '
                'Gritam o que sentem ou guardam tudo ate nao aguentar mais. Os dois machucam.',
                {'style': 'quote', 'text': 'Comunicacao madura nao e sobre "falar bonito". E sobre falar de um jeito que o outro consiga ouvir.'},
                {'style': 'heading', 'text': 'Os 4 erros fatais de comunicacao'},
                {'style': 'numbered', 'items': [
                    'ACUSAR: "Voce nunca me respeita", "Voce sempre faz isso". A palavra "voce" como ataque coloca o outro na defensiva imediatamente.',
                    'GENERALIZAR: "Sempre", "nunca", "toda vez". Generalizacoes transformam um problema especifico em uma acusacao de carater.',
                    'TRAZER O PASSADO: Usar erros antigos como municao. Quando voce traz o passado, a mensagem que ela ouve e "eu nunca vou te perdoar".',
                    'SILENCIO PUNITIVO: Parar de falar como forma de castigar. Voce acha que esta "se controlando", mas na verdade esta comunicando: "voce nao merece minha atencao".',
                ]},
            ]
        },
        {
            'title': 'A formula da comunicacao madura',
            'body': [
                'Existe uma estrutura simples que funciona em 90% das situacoes de conflito. '
                'Nao e magica. E tecnica. E como qualquer tecnica, melhora com a pratica.',
                {'style': 'heading', 'text': 'O modelo: EU SINTO + QUANDO + PRECISO'},
                {'style': 'card', 'height': 90, 'label': 'ESTRUTURA',
                 'text': '1. EU SINTO [emocao] - Nomeie o que voce sente. Sem acusar.\n2. QUANDO [situacao] - Descreva o fato, nao a interpretacao.\n3. PRECISO [pedido] - Diga o que precisa, nao o que ela fez de errado.'},
                {'style': 'heading', 'text': 'Exemplos praticos'},
                {'style': 'transformation', 'before': '"Voce nao me respeita"', 'after': '"Eu me sinto desvalorizado quando minhas opinioes sao ignoradas"'},
                {'style': 'transformation', 'before': '"Voce vive no celular"', 'after': '"Eu sinto falta da sua atencao quando estamos juntos"'},
                {'style': 'transformation', 'before': '"Voce deu mole pra ele"', 'after': '"Eu me senti inseguro naquela situacao e preciso conversar"'},
                '',
                {'style': 'heading', 'text': 'A arte de ouvir sem se defender'},
                'Comunicacao nao e so falar. E ouvir. E a parte mais dificil para homens inseguros, '
                'porque tudo que ela diz parece um ataque.',
                {'style': 'bullet', 'items': [
                    'Escute o que ela esta DIZENDO, nao o que voce acha que ela QUER DIZER.',
                    'Nao prepare sua resposta enquanto ela fala. Apenas escute.',
                    'Repita o que voce entendeu antes de responder: "Entao voce esta dizendo que..."',
                    'Se sentir que vai explodir, diga: "Preciso de 10 minutos para processar isso". E volte.',
                ]},
            ]
        },
        {
            'title': 'Exercicio: Conversas que constroem',
            'body': [
                {'style': 'exercise_header'},
                {'style': 'heading', 'text': 'Parte 1: Reescrevendo conflitos'},
                'Pense em 3 discussoes recentes. Para cada uma, reescreva o que voce disse usando '
                'a formula EU SINTO + QUANDO + PRECISO:',
                {'style': 'numbered', 'items': [
                    'O que voce disse na hora:',
                    'O que voce realmente estava sentindo:',
                    'Reescreva usando a formula:',
                ]},
                'Faca isso com as 3 situacoes. Observe como a mesma mensagem pode ser transmitida '
                'sem ataque e sem defesa.',
                {'style': 'heading', 'text': 'Parte 2: A conversa de abertura'},
                'Se voce sente que e hora de falar com ela sobre o que voce esta passando, '
                'use este roteiro como base:',
                {'style': 'card', 'height': 120, 'label': 'ROTEIRO SUGERIDO',
                 'text': '"Eu quero te falar uma coisa que nao e facil de dizer. Eu tenho trabalhado em entender minha inseguranca. Sei que as vezes reajo de formas que te machucam, e nao e isso que eu quero. Nao to pedindo pra voce resolver. To pedindo pra voce saber que estou tentando. E que o que eu sinto nao e culpa sua."'},
                '',
                'Voce nao precisa usar essas palavras exatas. Mas a estrutura importa: '
                'vulnerabilidade sem cobranca, honestidade sem acusacao, pedido sem exigencia.',
            ]
        },
    ]


def build_conclusion(c):
    c.showPage()
    draw_bg(c)

    draw_text(c, 'CONCLUSAO', 50, H - 70, 'Helvetica', 9, MUTED)
    draw_line(c, 50, H - 78, 120, H - 78, EMBER, 1)

    draw_text(c, 'O caminho adiante', 50, H - 120, 'Helvetica-Bold', 28, TEXT)

    y = draw_wrapped_text(c,
        'Se voce chegou ate aqui, ja fez mais do que a maioria dos homens faria. '
        'Voce olhou para si mesmo. Reconheceu padroes. Entendeu mecanismos. '
        'E tem ferramentas reais para mudar.',
        50, H - 170, 'Helvetica', 12, LIGHT_TEXT, max_width=460, leading=20)

    y = draw_wrapped_text(c,
        'Mas ler nao e o suficiente. O treinamento so funciona se voce pratica. '
        'Os exercicios existem para isso. Nao pule. Nao adie. Nao espere "o momento certo". '
        'O momento certo e agora.',
        50, y - 16, 'Helvetica', 11, DIM_TEXT, max_width=460, leading=18)

    y -= 16
    draw_text(c, 'O que voce aprendeu:', 50, y, 'Helvetica-Bold', 13, TEXT)
    y -= 24

    items = [
        'A inseguranca tem origem. E conhecer a origem e o primeiro passo para nao ser controlado por ela.',
        'A comparacao e um jogo viciado. Voce pode desligar o radar.',
        'A validacao externa nunca sera suficiente. A base precisa ser interna.',
        'O ciume pode ser interrompido. O Protocolo de 90 Segundos funciona.',
        'Comportamentos destrutivos parecem normais mas acumulam destruicao.',
        'Confianca real vem de 4 pilares que voce pode construir, dia apos dia.',
        'Comunicacao madura e uma habilidade. E habilidades se treinam.',
    ]

    for item in items:
        if y < 100:
            c.showPage()
            draw_bg(c)
            y = H - 60
        draw_circle_bullet(c, 58, y)
        y = draw_wrapped_text(c, item, 72, y, 'Helvetica', 11, DIM_TEXT, max_width=440, leading=18)
        y -= 8

    y -= 16
    draw_line(c, 55, y + 8, 55, y - 30, EMBER_GLOW, 2)
    y = draw_wrapped_text(c,
        'Nao e sobre virar outro homem. E sobre parar de sabotar quem voce ja e.',
        70, y, 'Helvetica-BoldOblique', 13, LIGHT_TEXT, max_width=430, leading=20)

    # Last page
    c.showPage()
    draw_bg(c)

    # Centered closing
    draw_line(c, W/2 - 25, H/2 + 100, W/2 + 25, H/2 + 100, EMBER, 2)

    c.setFont('Helvetica-Bold', 28)
    c.setFillColor(TEXT)
    text = 'O Homem Inseguro'
    tw = c.stringWidth(text, 'Helvetica-Bold', 28)
    c.drawString((W - tw) / 2, H/2 + 50, text)

    c.setFont('Helvetica', 12)
    c.setFillColor(LIGHT_TEXT)
    text2 = 'Voce ja deu o primeiro passo.'
    tw2 = c.stringWidth(text2, 'Helvetica', 12)
    c.drawString((W - tw2) / 2, H/2 + 20, text2)

    c.setFont('Helvetica', 11)
    c.setFillColor(DIM_TEXT)
    text3 = 'Agora e sobre consistencia.'
    tw3 = c.stringWidth(text3, 'Helvetica', 11)
    c.drawString((W - tw3) / 2, H/2 - 5, text3)

    draw_line(c, W/2 - 25, H/2 - 40, W/2 + 25, H/2 - 40, EMBER, 2)

    c.setFont('Helvetica', 9)
    c.setFillColor(SUBTLE)
    text4 = 'www.ohomeminseguro.store'
    tw4 = c.stringWidth(text4, 'Helvetica', 9)
    c.drawString((W - tw4) / 2, 80, text4)

    text5 = 'Este material tem finalidade educacional. Nao substitui acompanhamento profissional.'
    tw5 = c.stringWidth(text5, 'Helvetica', 9)
    c.drawString((W - tw5) / 2, 60, text5)


# ═══════════════════════════════════════════════════
# MAIN BUILD
# ═══════════════════════════════════════════════════

def build_pdf():
    output_path = '/Users/hrqcred/Desktop/projetos/ohomeminseguro/O-Homem-Inseguro-Treinamento.pdf'
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle('O Homem Inseguro - Treinamento')
    c.setAuthor('O Homem Inseguro')
    c.setSubject('Treinamento Digital - Inseguranca Masculina')

    # Cover
    build_cover(c)

    # Intro
    build_intro(c)

    # Sumario
    build_sumario(c)

    # Ciclo
    build_ciclo_page(c)

    # Module 01
    build_module_cover(c, '01', 'A origem da inseguranca',
                       'De onde vem esse medo que parece nao ter\nexplicacao. As raizes que ninguem te contou.')
    build_module_content(c, get_module_01())

    # Module 02
    build_module_cover(c, '02', 'O jogo da comparacao',
                       'Por que voce se mede contra outros homens\ne sempre perde. Como desligar esse radar.')
    build_module_content(c, get_module_02())

    # Module 03
    build_module_cover(c, '03', 'A armadilha da validacao',
                       'A dependencia silenciosa de ser aprovado.\nPor que nenhum elogio e suficiente.')
    build_module_content(c, get_module_03())

    # Module 04
    build_module_cover(c, '04', 'Ciume: o monstro familiar',
                       'O que o ciume realmente e, de onde ele vem\ne o mapa para desarmar o gatilho.')
    build_module_content(c, get_module_04())

    # Module 05
    build_module_cover(c, '05', 'Comportamentos que afastam',
                       'O inventario honesto de tudo que voce faz\nachando que protege e que na verdade destroi.')
    build_module_content(c, get_module_05())

    # Module 06
    build_module_cover(c, '06', 'Confianca interna',
                       'Como construir uma seguranca que nao depende\ndela, dos outros ou das circunstancias.')
    build_module_content(c, get_module_06())

    # Module 07
    build_module_cover(c, '07', 'Comunicacao madura',
                       'Falar o que sente sem acusar. Ouvir sem se\ndefender. A habilidade que salva relacionamentos.')
    build_module_content(c, get_module_07())

    # Conclusion
    build_conclusion(c)

    c.save()
    print(f'PDF gerado: {output_path}')

if __name__ == '__main__':
    build_pdf()
