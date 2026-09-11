import pytest
from src.email_service import email_valido

def test_email_valido_sucesso():
    """Valida e-mails corretos."""
    assert email_valido("cliente@empresa.com") is True
    assert email_valido("usuario.sobrenome@sub.dominio.com.br") is True

def test_email_invalido_sem_arroba():
    """Valida rejeição de e-mail sem @."""
    assert email_valido("clienteempresa.com") is False

def test_email_invalido_sem_dominio():
    """Valida rejeição de e-mail sem domínio ou extensão."""
    assert email_valido("cliente@") is False
    assert email_valido("cliente@dominio") is False

def test_email_com_espacos_ou_vazio():
    """Valida rejeição de strings vazias ou nulas."""
    assert email_valido("") is False
    assert email_valido("   ") is False