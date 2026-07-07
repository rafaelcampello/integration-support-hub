import xml.etree.ElementTree as ET


def xml_to_dict(xml_text: str) -> dict:
    """Converte XML simples em dicionário para resposta JSON padronizada."""

    root = ET.fromstring(xml_text)
    return {
        "tag": root.tag,
        "children": {child.tag: child.text for child in root},
    }


def build_customer_query_xml(customer_id: int = 123) -> str:
    """Monta um XML mínimo para simular uma consulta SOAP."""

    return f"""<Envelope>
  <Body>
    <ConsultarCliente>
      <ClienteId>{customer_id}</ClienteId>
    </ConsultarCliente>
  </Body>
</Envelope>"""
