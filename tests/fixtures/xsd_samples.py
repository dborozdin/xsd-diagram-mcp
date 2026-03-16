"""XSD schema samples for tests — string constants written to tmp_path at runtime."""

SIMPLE_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Name" type="xs:string"/>
</xs:schema>
"""

COMPLEX_TYPE_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Person" type="PersonType"/>
  <xs:complexType name="PersonType">
    <xs:sequence>
      <xs:element name="FirstName" type="xs:string"/>
      <xs:element name="LastName" type="xs:string"/>
      <xs:element name="Age" type="xs:int" minOccurs="0"/>
    </xs:sequence>
    <xs:attribute name="id" type="xs:string" use="required"/>
  </xs:complexType>
</xs:schema>
"""

CHOICE_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Payment" type="PaymentType"/>
  <xs:complexType name="PaymentType">
    <xs:choice>
      <xs:element name="CreditCard" type="xs:string"/>
      <xs:element name="BankTransfer" type="xs:string"/>
      <xs:element name="Cash" type="xs:string"/>
    </xs:choice>
  </xs:complexType>
</xs:schema>
"""

ENUM_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Color" type="ColorType"/>
  <xs:simpleType name="ColorType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="Red"/>
      <xs:enumeration value="Green"/>
      <xs:enumeration value="Blue"/>
    </xs:restriction>
  </xs:simpleType>
</xs:schema>
"""

NESTED_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Level0" type="Level0Type"/>
  <xs:complexType name="Level0Type">
    <xs:sequence>
      <xs:element name="Level1" type="Level1Type"/>
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="Level1Type">
    <xs:sequence>
      <xs:element name="Level2" type="Level2Type"/>
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="Level2Type">
    <xs:sequence>
      <xs:element name="Level3" type="Level3Type"/>
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="Level3Type">
    <xs:sequence>
      <xs:element name="Level4" type="Level4Type"/>
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="Level4Type">
    <xs:sequence>
      <xs:element name="Level5" type="Level5Type"/>
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="Level5Type">
    <xs:sequence>
      <xs:element name="Level6" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>
</xs:schema>
"""

NAMESPACE_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://example.com/test"
           xmlns:tns="http://example.com/test"
           elementFormDefault="qualified">
  <xs:element name="Document" type="tns:DocumentType"/>
  <xs:complexType name="DocumentType">
    <xs:sequence>
      <xs:element name="Title" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>
</xs:schema>
"""

ABSTRACT_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Shape" type="ShapeType" abstract="true"/>
  <xs:complexType name="ShapeType" abstract="true">
    <xs:sequence>
      <xs:element name="Color" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>
  <xs:element name="Circle" substitutionGroup="Shape" type="CircleType"/>
  <xs:complexType name="CircleType">
    <xs:complexContent>
      <xs:extension base="ShapeType">
        <xs:sequence>
          <xs:element name="Radius" type="xs:double"/>
        </xs:sequence>
      </xs:extension>
    </xs:complexContent>
  </xs:complexType>
</xs:schema>
"""

IMPORT_TYPES_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://example.com/types"
           xmlns:tns="http://example.com/types"
           elementFormDefault="qualified">
  <xs:complexType name="AddressType">
    <xs:sequence>
      <xs:element name="Street" type="xs:string"/>
      <xs:element name="City" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>
</xs:schema>
"""

IMPORT_MAIN_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:types="http://example.com/types">
  <xs:import namespace="http://example.com/types" schemaLocation="types.xsd"/>
  <xs:element name="Order">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Id" type="xs:string"/>
        <xs:element name="ShipTo" type="types:AddressType"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""

MALFORMED_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Broken"
  <!-- missing closing tag -->
"""

MULTI_ELEMENT_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Alpha" type="xs:string"/>
  <xs:element name="Beta" type="xs:int"/>
  <xs:element name="Gamma" type="xs:date"/>
</xs:schema>
"""

MULTILANG_XSD = """\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:annotation>
    <xs:documentation xml:lang="en">Schema with multilingual annotations.</xs:documentation>
    <xs:documentation xml:lang="ru">Схема с мультиязычными аннотациями.</xs:documentation>
  </xs:annotation>
  <xs:element name="Greeting" type="xs:string">
    <xs:annotation>
      <xs:documentation xml:lang="en">Hello</xs:documentation>
      <xs:documentation xml:lang="ru">Привет</xs:documentation>
    </xs:annotation>
  </xs:element>
  <xs:element name="Farewell" type="xs:string">
    <xs:annotation>
      <xs:documentation xml:lang="en">Goodbye</xs:documentation>
      <xs:documentation xml:lang="ru">До свидания</xs:documentation>
    </xs:annotation>
  </xs:element>
</xs:schema>
"""
