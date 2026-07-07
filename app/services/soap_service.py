from app.utils.xml_utils import build_customer_query_xml, xml_to_dict


def call_simulated_soap_service() -> tuple[str, dict]:
    """Simula uma chamada SOAP sem depender de serviço externo.

    A ideia é mostrar o fluxo mental do suporte: montar XML, receber XML e
    traduzir a resposta para JSON para facilitar análise por clientes REST.
    """

    request_xml = build_customer_query_xml()
    response_xml = """<ConsultarClienteResponse>
  <ClienteId>123</ClienteId>
  <Nome>Cliente Demonstração</Nome>
  <Status>Ativo</Status>
  <Mensagem>Consulta SOAP simulada com sucesso.</Mensagem>
</ConsultarClienteResponse>"""
    return request_xml, xml_to_dict(response_xml)
