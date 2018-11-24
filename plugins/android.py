'''
! Não implementada
'''
from plyer import notification, vibrator
from plyer.utils import platform
from plyer.compat import PY2

class Android():

    def notificar(self, titulo, mensagem, rotulo='', modo='normal', icone='plyer-icon', tempo=4):
        try:
            if PY2:
                titulo = titulo.decode('utf8')
                mensagem = mensagem.decode('utf8')
            kwargs = {'title': titulo, 'message': mensagem, 'ticker': rotulo}

            if (modo == 'chique'):
                kwargs['app_name'] = 'Notificação'
                
                if (platform == 'win'):
                    kwargs['app_icon'] = 'imagens/sistema/{}.ico'.format(icone)
                    kwargs['timeout'] = tempo
                else:
                    kwargs['app_icon'] = 'imagens/sistema/{}.png'.format(icone)
            
            notification.notify(**kwargs)
        except Exception as e:
            print('Falha ao notificar', str(e))

    def vibrar(self, tempo=1):
        try:
            print(vibrator.exists())
            if (vibrator.exists()):
                vibrator.vibrate(tempo)
        except Exception as e:
            print('Falha ao vibrar', str(e))