from flask import Flask, render_template, request, jsonify
from scipy.optimize import linprog

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Valores padrão iniciais
    dados = {
        'm_desk': 8000, 'm_note': 1000, 'm_net': 2000, 'm_custo': 150000,
        's_desk': 2000, 's_note': 1000, 's_net': 7000, 's_custo': 210000,
        'd_desk': 16000, 'd_note': 6000, 'd_net': 28000
    }
    
    resultado = None

    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        for chave in dados.keys():
            dados[chave] = int(request.form.get(chave, dados[chave]))

        # Configura o solver do Scipy
        c = [dados['m_custo'], dados['s_custo']]
        A = [
            [-dados['m_desk'], -dados['s_desk']],
            [-dados['m_note'], -dados['s_note']],
            [-dados['m_net'], -dados['s_net']]
        ]
        b = [-dados['d_desk'], -dados['d_note'], -dados['d_net']]
        
        res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')
        
        if res.success:
            resultado = {
                'sucesso': True,
                'x': round(res.x[0], 2),
                'y': round(res.x[1], 2),
                'custo': f"R$ {res.fun:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            }
        else:
            resultado = {'sucesso': False, 'erro': 'Não foi possível encontrar uma solução viável.'}

    return render_template('index.html', dados=dados, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)