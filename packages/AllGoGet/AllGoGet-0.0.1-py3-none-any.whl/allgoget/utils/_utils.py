import MetaTrader5 as mt5
import pandas as pd
from IPython.display import display 

__all__ = ["iniciar", "info_conta"]

def iniciar(login, server, password):
    '''
    Função utilizada para logar na conta e conectar ao MT5

    Parameters
    ----------
    login : int, optional
        Login da conta.
    server : string, optional
        Servidor da corretora.
    password : string, optional
        Senha da conta.

    Returns
    -------
    None.
    
    Example
    -------
    iniciar(login=00000000, server="XXXXX",password="XXXXXX")

    '''
    # Display data on the MetaTrader 5 package
    print("MetaTrader5 package author: ",mt5.__author__)
    print("MetaTrader5 package version: ",mt5.__version__)
    # establish MetaTrader 5 connection to a specified trading account
    if not mt5.initialize(login=login,server=server,password=password):
        print("initialize() failed, error code =",mt5.last_error())
        #quit()
    # display data on connection status, server name and trading account
    terminal_info=mt5.terminal_info()
    if terminal_info!=None:
        # display trading terminal data in the form of a dictionary
        terminal_info = (pd.DataFrame(terminal_info
                                     ._asdict()
                                     .items(),
                                     columns=['property','value'])
                         [2:19])       
        display(terminal_info)
    else:
        print("failed to connect to trade terminal_info, error code =",
              mt5.last_error())
    #display data on MetaTrader 5 version
    print(mt5.version())


def info_conta():
    '''
    Função utilizada para apresentar informações da conta logada

    Returns
    -------
    None.

    '''
    account_info=mt5.account_info()
    if account_info!=None:
        # display trading account data in the form of a dictionary
        account_info = pd.DataFrame(account_info
                                    ._asdict()
                                    .items(),
                                    columns=['property','value'])
        display(account_info)
    else:
        print("failed to connect to trade account, error code =",mt5.last_error())
