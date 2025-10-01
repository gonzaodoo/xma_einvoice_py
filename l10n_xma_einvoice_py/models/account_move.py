# -*- coding: utf-8 -*-
from odoo import fields, models, _
import json
from datetime import datetime
from random import choice, randint
import asyncio
import time
# import asyncio_gevent

from nio import AsyncClient, RoomMessageText, RoomMessageFile
import simplematrixbotlib as botlib
class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_xma_use_document_id = fields.Many2one(
        'l10n_xma.use.document',
        string='Use Document'
    )    
    l10n_xma_payment_type_id = fields.Many2one(
        'l10n_xma.payment_type',
        string='EDI Payment Type'
    )
    l10n_xma_edi_legal_status_id = fields.Many2one(
        'l10n_xma.edi.legal.status',
        string='EDI Legal Status'
    )
    l10n_xma_edi_related = fields.Char(
        string='EDI Related'
    )
    
    is_einvoice_send = fields.Boolean(string="Timbrado", copy=False)
    
    l10n_xma_origin_operation_id = fields.Many2one(
        'l10n_xma.origin_operation',
        string='Use Document'
    )    
    
    l10n_xma_issuance_type_id = fields.Many2one(
        'l10n_xma.issuance_type',
        string='Use Document'
    )    
    
    l10n_xma_edi_einvoice  = fields.Char(readonly=True, copy=False)
    
    l10n_xma_payment_form_id = fields.Many2one(
        'xma_payment.form',
        string='Use Document'
    )
    l10n_xma_document_type = fields.Many2one(
        'l10n_latam.document.type', string="Tipo de Documento"
    )

    ramdom_code = fields.Char(readonly=True, copy=False)
    l10n_xma_cdc_code = fields.Char("Código de control (CDC)")


    def action_post(self):
        self._generate_pin()
        return super(AccountMove, self).action_post()
    
    def send_to_matrix_json(self):
        xml_json_py = self.generate_json_l10n_py()
        xml_json_mx = self.generate_json_l10n_mx()
        # xml_json = '{"PY":{"id":1,"uuid_client":"Xmarts:00002","params":{"version":150,"fechaFirmaDigital":"2023-03-07T00:00:00","ruc":"80016658-2","razonSocial":"ASISMED SA","nombreFantasia":"ASISMED","actividadesEconomicas":[{"codigo":"1254","descripcion":"Desarrollo de Software"}],"timbradoNumero":"12558946","timbradoFecha":"2022-08-25","tipoContribuyente":2,"tipoRegimen":8,"establecimientos":[{"codigo":"001","direccion":"Barrio Carolina","numeroCasa":"0","complementoDireccion1":"Entre calle 2","complementoDireccion2":"y Calle 7","departamento":11,"departamentoDescripcion":"ALTO PARANA","distrito":145,"distritoDescripcion":"CIUDAD DEL ESTE","ciudad":3432,"ciudadDescripcion":"PUERTO PTE.STROESSNER (MUNIC)","telefono":"0973-527155","email":"tips@tips.com.py, tips@gmail.com","denominacion":"Sucursal 1"}]},"data":{"tipoDocumento":1,"establecimiento":"001","codigoSeguridadAleatorio":"298398","punto":"001","numero":"0000001","descripcion":"Aparece en el documento","observacion":"Cualquier informacion de marketing, publicidad, sorteos, promociones para el Receptor","fecha":"2022-08-14T10:11:00","tipoEmision":1,"tipoTransaccion":1,"tipoImpuesto":1,"moneda":"PYG","condicionAnticipo":1,"condicionTipoCambio":1,"descuentoGlobal":0,"cambio":6700,"cliente":{"contribuyente":true,"ruc":"20050011-1","razonSocial":"Marcos Adrian Jara Rodriguez","nombreFantasia":"Marcos Adrian Jara Rodriguez","tipoOperacion":1,"direccion":"Avda Calle Segunda y Proyectada","numeroCasa":"1515","departamento":11,"departamentoDescripcion":"ALTO PARANA","distrito":143,"distritoDescripcion":"DOMINGO MARTINEZ DE IRALA","ciudad":3344,"ciudadDescripcion":"PASO ITA (INDIGENA)","pais":"PRY","paisDescripcion":"Paraguay","tipoContribuyente":1,"documentoTipo":1,"documentoNumero":"2324234","telefono":"061-575903","celular":"0973-809103","email":"cliente@empresa.com, cliente@personal.com","codigo":"1548"},"usuario":{"documentoTipo":1,"documentoNumero":"157264","nombre":"Marcos Jara","cargo":"Vendedor"},"factura":{"presencia":1,"fechaEnvio":"2023-10-21","dncp":{"modalidad":"ABC","entidad":1,"año":2021,"secuencia":3377,"fecha":"2022-09-14T10:11:00"}},"autoFactura":{"tipoVendedor":1,"documentoTipo":1,"documentoNumero":1,"nombre":"Vendedor autofactura","direccion":"Vendedor autofactura","numeroCasa":"Vendedor autofactura","departamento":11,"departamentoDescripcion":"ALTO PARANA","distrito":143,"distritoDescripcion":"DOMINGO MARTINEZ DE IRALA","ciudad":3344,"ciudadDescripcion":"PASO ITA (INDIGENA)","transaccion":{"lugar":"Donde se realiza la transaccion","departamento":11,"departamentoDescripcion":"ALTO PARANA","distrito":143,"distritoDescripcion":"DOMINGO MARTINEZ DE IRALA","ciudad":3344,"ciudadDescripcion":"PASO ITA (INDIGENA)"}},"notaCreditoDebito":{"motivo":1},"remision":{"motivo":1,"tipoResponsable":1,"kms":150,"fechaFactura":"2022-08-21"},"condicion":{"tipo":1,"entregas":[{"tipo":1,"monto":"150000","moneda":"PYG","cambio":0},{"tipo":3,"monto":"150000","moneda":"PYG","cambio":0,"infoTarjeta":{"tipo":1,"tipoDescripcion":"Dinelco","titular":"Marcos Jara","ruc":"5448675-0","razonSocial":"Bancard","medioPago":1,"codigoAutorizacion":232524234}},{"tipo":2,"monto":"150000","moneda":"PYG","cambio":0,"infoCheque":{"numeroCheque":"32323232","banco":"Sudameris"}}],"credito":{"tipo":1,"plazo":"30 días","cuotas":2,"montoEntrega":1500000,"infoCuotas":[{"moneda":"PYG","monto":800000,"vencimiento":"2021-10-30"},{"moneda":"PYG","monto":800000,"vencimiento":"2021-11-30"}]}},"items":[{"codigo":"A-001","descripcion":"Producto o Servicio","observacion":"Información adicional o complementaria sobre el producto","partidaArancelaria":4444,"ncm":"ABCD1234","unidadMedida":77,"cantidad":10.5,"precioUnitario":10800,"cambio":0,"descuento":0,"anticipo":0,"pais":"PRY","paisDescripcion":"Paraguay","tolerancia":1,"toleranciaCantidad":1,"toleranciaPorcentaje":1,"dncp":{"codigoNivelGeneral":"12345678","codigoNivelEspecifico":"1234","codigoGtinProducto":"12345678","codigoNivelPaquete":"12345678"},"ivaTipo":1,"ivaBase":100,"iva":5,"lote":"A-001","vencimiento":"2022-10-30","numeroSerie":"","numeroPedido":"","numeroSeguimiento":"","importador":{"nombre":"Importadora Parana S.A.","direccion":"Importadora Parana S.A.","registroImportador":"Importadora Parana S.A."},"registroSenave":"323223","registroEntidadComercial":"RI-32/22","sectorAutomotor":{"tipo":1,"chasis":"45252345235423532","color":"Rojo","potencia":1500,"capacidadMotor":5,"capacidadPasajeros":5,"pesoBruto":10000,"pesoNeto":8000,"tipoCombustible":9,"tipoCombustibleDescripcion":"Vapor","numeroMotor":"323234234234234234","capacidadTraccion":151.01,"año":2009,"tipoVehiculo":"Camioneta","cilindradas":"3500"}}],"sectorEnergiaElectrica":{"numeroMedidor":"132423424235425","codigoActividad":125,"codigoCategoria":"001","lecturaAnterior":4,"lecturaActual":5},"sectorSeguros":{"codigoAseguradora":"","codigoPoliza":"AAAA","numeroPoliza":"BBBB","vigencia":1,"vigenciaUnidad":"año","inicioVigencia":"2023-03-01","finVigencia":"2022-10-01","codigoInternoItem":"A-001"},"sectorSupermercados":{"nombreCajero":"Juan Antonio Caceres","efectivo":150000,"vuelto":30000,"donacion":1000,"donacionDescripcion":"Donado para la caridad"},"sectorAdicional":{"ciclo":"Mensualidad","inicioCiclo":"2023-02-01","finCiclo":"2023-03-01","vencimientoPago":"2023-03-07","numeroContrato":"AF-2541","saldoAnterior":1550000}},"usuario":{"documentoTipo":false,"documentoNumero":"INV/2023/00001","nombre":"Administrator","cargo":"Vendedor"},"factura":{},"autoFactura":{},"notaCreditoDebito":{},"remision":{},"condicion":{},"items":[{"codigo":"00342","descripcion":"coca-cola lite 400ml","observacion":"coca","unidadMedida":"Unidades","cantidad":1,"precioUnitario":1,"cambio":0,"descuento":0,"anticipo":0,"pais":"MX","paisDescripcion":"México","tolerancia":1,"toleranciaCantidad":1,"toleranciaPorcentaje":1,"dncp":{},"ivaTipo":1,"ivaBase":100,"iva":5,"lote":"A-001","vencimiento":"2022-10-30","numeroSerie":"","numeroPedido":"","numeroSeguimiento":"","importador":{},"registroSenave":"323223","registroEntidadComercial":"RI-32/22","sectorAutomotor":{}}],"sectorEnergiaElectrica":{},"sectorSeguros":{},"sectorSupermercados":{},"sectorAdicional":{}},"MX":{"id":1,"uuid_client":"dsfnsefsxdv","data":{"xsi:schemaLocation":"http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd http://www.sat.gob.mx/ComercioExterior11 http://www.sat.gob.mx/sitio_internet/cfd/ComercioExterior11/ComercioExterior11.xsd","xmlns:cfdi":"http://www.sat.gob.mx/cfd/3","xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance","xmlns:cce11":"http://www.sat.gob.mx/ComercioExterior11","Version":"3.3","Fecha":"2022-12-07T12:10:33","Folio":0,"Serie":"","Sello":"","FormaPago":false,"NoCertificado":"","Certificado":"","CondicionesDePago":"30 días","SubTotal":"20338.00","Descuento":0,"Moneda":"MXN","TipoCambio":{},"Total":"23592.07","TipoDeComprobante":"I","MetodoPago":"","LugarExpedicion":"94134","cfdi:CfdiRelacionados":[],"cfdi:Emisor":{"Rfc":false,"Nombre":"My Company (San Francisco)","RegimenFiscal":false},"cfdi:Receptor":{"Rfc":false,"Nombre":"Deco Addict","UsoCFDI":false},"cfdi:Conceptos":[{"cfdi:Concepto":{"ClaveProdServ":"10101500","NoIdentificacion":"FURN_8999","Cantidad":"5.000000","ClaveUnidad":"18","Unidad":"Unidades","Descripcion":"[FURN_8999] Sofá de tres asientos Sofá de tres plazas con tumbona en color gris acero","ValorUnitario":"1500.00","Importe":"7500.00","Descuento":"0.00","cfdi:Impuestos":{"cfdi:Traslados":[{"cfdi:Traslado":{"Base":"7500.00","Impuesto":"002","TipoFactor":false,"TasaOCuota":"0.160000","Importe":"1200.00"}}],"cfdi:Retenciones":[]}}}],"cfdi:Impuestos":{"TotalImpuestosTrasladados":3254.070000000001,"TotalImpuestosRetenidos":0,"cfdi:Retenciones":[],"cfdi:Traslados":[{"cfdi:Traslado":{"Importe":3254.070000000001,"Impuesto":"002","TipoFactor":false,"TasaOCuota":"0.160000"}}]}}}}'
        xml_json = '{"PY":'+xml_json_py+',"MX":'+xml_json_mx+'}'

        # xml_json = json.dumps(json.loads(xml_json), default=str) XML TEST
        #xml_json = json.dumps(xml_json, default=str, indent=0, ensure_ascii=False, separators=(',', ':'))
        print(xml_json)
        asyncio.run(self.async_send_message(xml_json.encode('utf-8').decode('unicode_escape')))
        count = 0
        while count <= 3:
            print(count)
            self.refresh_account_move_xma()
            time.sleep(4)
            print("Se Ejecuto!!!")
            count += 1

    def refresh_account_move_xma(self):
        print("REFRESH ACCOUNT")
        return {
            'name': _("Facturacion"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'domain': [('id', '=', self.id)],
            'target': 'current',
            'res_id': self.id,
        }
    
    async def async_send_message(self, json):    
        server = self.company_id.matrix_server
        user = self.company_id.matrix_user
        password = self.company_id.matrix_password
        room_id = self.company_id.matrix_room

        client = AsyncClient(
            server,
            user,
            # "david.diaz",
            config={}
        ) 
        await client.login(password)
        # await client.login("gatitomaloxd")
        await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                # "body": f'#stamp {json[1: -1]}',
                "body": f'#stamp {str(json)}',
            }
        )
        await client.close()

    def generate_cdc(self):
        for rec in self:
            cdc = ''
            document_type = '0' +  str(rec.l10n_xma_document_type.code)
            ruc = rec.partner_id.vat
            digit_v_ruc = rec.partner_id.l10n_xma_control_digit
            eto = rec.l10n_xma_document_type.l10n_xma_branch
            
            rec.l10n_xma_cdc_code = cdc

    def _generate_pin(self):

        pin_length = 9
        number_max = (10**pin_length) - 1
        number = randint(0, number_max)
        delta = (pin_length - len(str(number))) * '0'
        print('%s%s' % (delta, number))
        ramdom_code  = '%s%s' % (delta, number)
        condition = self.validate_ramdom_code(ramdom_code)
        if condition == True:
            self._generate_pin()
        self.ramdom_code = ramdom_code
    
    def validate_ramdom_code(self, code):
        acc = self.env['account.move'].search([('ramdom_code', '=', code)])
        if len(acc) >0:
            return True
        else: return False
        # def create_pin():
        #     pin_length = 9
        #     number_max = (10**pin_length) - 1
        #     number = randint(0, number_max)
        #     delta = (pin_length - len(str(number))) * '0'
        #     print('%s%s' % (delta, number))
        #     self.ramdom_code  = '%s%s' % (delta, number)
        #     return '%s%s' % (delta, number)
        # drivers = self.search_read(
        #     [('ramdom_code', '!=', False)],
        #     fields=['ramdom_code']
        # )
        # pins = [driver['ramdom_code'] for driver in drivers]
        # while True:
        #     pin = create_pin()
        #     if pin not in pins:
        #         break
        # return pin
    # def generate_random_code(self):
    #     longitud = 9
    #     numeros = "0123456789"
    #     key_ramdom= ""
    #     key_ramdom = key_ramdom.join(
    #         [choice(numeros)
    #             for i in range(longitud)]
    #     )
    #     if self.ramdom_code_compute != '':
    #         self.ramdom_code_compute = self.ramdom_code_compute
    #         self.ramdom_code = self.ramdom_code_compute
    #     else:
    #         self.ramdom_code = key_ramdom
    #         self.ramdom_code_compute = key_ramdom
    #     return key_ramdom
    # def validate_ramdom_code(self, code):
    #     ramdom = self.env['account.move'].search([('ramdom_code_compute', '=', code)])
    #     if len(ramdom) >0:
    #         return True
    #     else: return False
    def generate_json_l10n_py(self):

        res = super(AccountMove, self).generate_json_l10n_py()
        actividadesEco = []
        for activities in self.company_id.l10n_xma_economic_activity_campany_id:
            actividadesEco.append({
                "codigo": activities.code,
                "descripcion": activities.name,
            })
        
        country_lines = self.partner_id.country_id
        items = []
        for lines in self.invoice_line_ids:
            items.append({ 
                "codigo" : lines.product_id.default_code, #"A-001",
                "descripcion": lines.product_id.name, # "Producto o Servicio", 
                "observacion": lines.name, # "Información adicional o complementaria sobre el producto", 
                # "partidaArancelaria" : 4444,
                # "ncm": "ABCD1234",
                "unidadMedida":int(lines.product_id.uom_id.l10n_xma_uomcode_id.code), # 77,
                "cantidad":lines.quantity, # 10.5,
                "precioUnitario":lines.price_subtotal, #10800,
                "cambio": 0,
                "descuento":lines.discount_balance, #0,
                "anticipo": 0,
                "pais" :country_lines.l10n_xma_country_code,
                "paisDescripcion" : country_lines.name, # "Paraguay",
                # "tolerancia" : 1,
                # "toleranciaCantidad" : 1,
                # "toleranciaPorcentaje" : 1,
                #"cdcAnticipo" : "44digitos",
                "dncp" : [],
                #     "codigoNivelGeneral" : "12345678",
                #     "codigoNivelEspecifico" : "1234",
                #     "codigoGtinProducto" : "12345678",
                #     "codigoNivelPaquete" : "12345678"
                # },
                "ivaTipo" : int(lines.tax_ids.l10n_xma_edi_tax_type_id.code), # Revisar
                "ivaBase" : int(lines.tax_ids.l10n_xma_base_tax),
                "iva" : int(lines.tax_ids.amount),
                # "lote" : "A-001",
                # "vencimiento" : "2022-10-30",
                # "numeroSerie" : "",
                # "numeroPedido" : "",
                # "numeroSeguimiento" : "",
                # "importador" : {
                #     "nombre" : "Importadora Parana S.A.",
                #     "direccion" : "Importadora Parana S.A.",
                #     "registroImportador" : "Importadora Parana S.A."
                # },
                # "registroSenave" : "323223",
                # "registroEntidadComercial" : "RI-32/22",
                # "sectorAutomotor" : {
                #     "tipo" : 1,
                #     "chasis" : "45252345235423532",
                #     "color" : "Rojo",
                #     "potencia" : 1500,
                #     "capacidadMotor" : 5,
                #     "capacidadPasajeros" : 5,
                #     "pesoBruto" : 10000,
                #     "pesoNeto" : 8000,
                #     "tipoCombustible" : 9,
                #     "tipoCombustibleDescripcion" : "Vapor",
                #     "numeroMotor" : "323234234234234234",
                #     "capacidadTraccion" : 151.01,
                #     "año" : 2009,
                #     "tipoVehiculo" : "Camioneta",
                #     "cilindradas" : "3500"
                # }
            })
        code = ''
        if not self.ramdom_code:
            code = self._generate_pin()
        tipoRegimen = int(self.company_id.partner_id.l10n_xma_taxpayer_type_id.code)
        datetime_firma = datetime.now().replace(microsecond=0)
        spl = str(datetime_firma).split(' ')
        str_time = str(spl[0] + 'T' + spl[1])
        json_params = {
            "version": int(self.journal_id.version_document),#150,
            "fechaFirmaDigital":str_time,#"2023-03-07T00:00:00",
            "ruc":self.company_id.partner_id.vat + '-' + self.company_id.partner_id.l10n_xma_control_digit,#"80016658-2",
            "razonSocial":self.company_id.name, #"ASISMED SA",
            "nombreFantasia":self.company_id.partner_id.name,#"ASISMED", # pendiente
            "actividadesEconomicas":actividadesEco,
            "timbradoNumero": self.l10n_xma_document_type.l10n_xma_authorization_code,#"12558946",
            "timbradoFecha":self.invoice_date, # "2022-08-25",
            "tipoContribuyente": 1 if self.company_id.partner_id.company_type == 'person' else 2,
            "tipoRegimen":tipoRegimen,
            "establecimientos":[{
                "codigo":self.journal_id.l10n_xma_latam_document_type_id.l10n_xma_branch, #"001",
                "direccion":self.journal_id.l10n_xma_invoice_dir_id.street, #"Barrio Carolina", 
                "numeroCasa":self.journal_id.l10n_xma_invoice_dir_id.l10n_xma_external_number,  #"0",
                "complementoDireccion1":self.journal_id.l10n_xma_invoice_dir_id.street, #"Entre calle 2", 
                "complementoDireccion2":self.journal_id.l10n_xma_invoice_dir_id.street2, #"y Calle 7",
                "departamento":int(self.journal_id.l10n_xma_invoice_dir_id.state_id.code), #11,
                "departamentoDescripcion":self.journal_id.l10n_xma_invoice_dir_id.state_id.name, #"ALTO PARANA",
                "distrito": int(self.journal_id.l10n_xma_invoice_dir_id.l10n_xma_municipality_id.code), #145,
                "distritoDescripcion":self.journal_id.l10n_xma_invoice_dir_id.l10n_xma_municipality_id.name, #"CIUDAD DEL ESTE",
                "ciudad": int(self.journal_id.l10n_xma_invoice_dir_id.l10n_xma_city_id.zipcode),#3432,
                "ciudadDescripcion":self.journal_id.l10n_xma_invoice_dir_id.l10n_xma_city_id.name,#"PUERTO PTE.STROESSNER (MUNIC)",
                "telefono":self.journal_id.l10n_xma_invoice_dir_id.phone or "",#"0973-527155",
                "email":self.journal_id.l10n_xma_invoice_dir_id.email or "", #"tips@tips.com.py, tips@gmail.com",
                "denominacion":self.journal_id.l10n_xma_invoice_dir_id.name, #"Sucursal 1",
            }]
        }
        numero_documento = self.name.split('/')
        json_data = {
            "tipoDocumento" : int(self.l10n_xma_document_type.code), #1,
            "establecimiento":self.l10n_xma_document_type.l10n_xma_branch, #"001",
            "codigoSeguridadAleatorio": self.ramdom_code if self.ramdom_code else code, #Generar Ramdom
            "punto" :self.l10n_xma_document_type.l10n_xma_dispatch_point, #"001",
            "numero":'00' + str(numero_documento[2]), #"0000001", 
            # "descripcion":"Aparece en el documento", #Valor por Defecto
            # "observacion": "Cualquier informacion de marketing, publicidad, sorteos, promociones para el Receptor", #Valor por Defecto
            "fecha":str_time,#"2022-08-14T10:11:00",
            "tipoEmision":int(self.l10n_xma_issuance_type_id.code), #1,
            "tipoTransaccion" : 1,#Valor por Defecto
            "tipoImpuesto" : 1, #Valor por Defecto
            "moneda" : self.currency_id.name, #"PYG",
            # "condicionAnticipo" : 0, #Valor por Defecto
            # "condicionTipoCambio": 0, # Valor por Defecto
            # "descuentoGlobal": 0, #Valor por Defecto
            # "anticipoGlobal": 0, #Valor por Defecto
            # "cambio": 6700,
            "cliente" : {
                "contribuyente":self.partner_id.l10n_xma_is_taxpayer, #True, # Buscar en odoo
                "ruc":self.partner_id.vat +'-'+ self.partner_id.l10n_xma_control_digit, # "20050011-1",
                "razonSocial" :self.partner_id.name, # "Marcos Adrian Jara Rodriguez",
                "nombreFantasia": self.partner_id.commercial_name, # "Marcos Adrian Jara Rodriguez",
                "tipoOperacion": int(self.partner_id.l10n_xma_customer_operation_type), #1, # Buscar en odoo
                "direccion":self.partner_id.street,# "Avda Calle Segunda y Proyectada",
                "numeroCasa":self.partner_id.l10n_xma_external_number, #  "1515",
                "departamento":self.partner_id.state_id.id,
                "departamentoDescripcion":self.partner_id.state_id.name, #"ALTO PARANA",
                "distrito":int(self.partner_id.l10n_xma_municipality_id.code),#143, # Buscar en odoo
                "distritoDescripcion":self.partner_id.l10n_xma_municipality_id.name, #"DOMINGO MARTINEZ DE IRALA",
                "ciudad": int(self.partner_id.l10n_xma_city_id.zipcode),
                "ciudadDescripcion":self.partner_id.l10n_xma_city_id.name,  #"PASO ITA (INDIGENA)",
                "pais":self.partner_id.country_id.l10n_xma_country_code, #"PRY",
                "paisDescripcion":self.partner_id.country_id.name, # "Paraguay",
                "tipoContribuyente":1, #int(self.partner_id.l10n_xma_taxpayer_type_id.code), #1, # buscar en odoo
                "documentoTipo":int(self.l10n_xma_document_type.code),#1, # buscar en odoo
                "documentoNumero":'00' + str(numero_documento[2]),# "2324234",
                # "telefono":self.partner_id.phone,# "061-575903",
                # "celular":self.partner_id.mobile,# "0973-809103",
                # "email":self.partner_id.email,#"cliente@empresa.com, cliente@personal.com",
                "codigo" : self.partner_id.ref# Buscar en odoo
            },
            "usuario" : {
                "documentoTipo": int(self.l10n_xma_document_type.code), # 1,
                "documentoNumero": self.env.user.identification_id, # "157264",
                "nombre":self.env.user.name,# "Marcos Jara",
                "cargo" : self.env.user.employee_id.job_id.name
            }, 
            "factura" : {
                "presencia" : 1,
                # "fechaEnvio" : "2023-10-21",
                # "dncp" : {
                #     "modalidad" : "ABC",
                #     "entidad" : 1,
                #     "año" : 2021,
                #     "secuencia" : 3377,
                #     "fecha" : "2022-09-14T10:11:00"
                # }
            },
            # "autoFactura" : [],
                # "tipoVendedor" : 1,
                # "documentoTipo" : 1,
                # "documentoNumero" : 1,
                # "nombre" : "Vendedor autofactura",
                # "direccion" : "Vendedor autofactura",
                # "numeroCasa" : "Vendedor autofactura",
                # "departamento" : 11,
                # "departamentoDescripcion" : "ALTO PARANA",
                # "distrito" : 143,
                # "distritoDescripcion" : "DOMINGO MARTINEZ DE IRALA",
                # "ciudad" : 3344,
                # "ciudadDescripcion" : "PASO ITA (INDIGENA)",
                # "transaccion" : {
                #     "lugar" : "Donde se realiza la transaccion",
                #     "departamento" : 11,
                #     "departamentoDescripcion" : "ALTO PARANA",
                #     "distrito" : 143,
                #     "distritoDescripcion" : "DOMINGO MARTINEZ DE IRALA",
                #     "ciudad" : 3344,
                #     "ciudadDescripcion" : "PASO ITA (INDIGENA)"
                # }
            # },
            # "notaCreditoDebito" : {
            #     "motivo" : 1
            # },
            # "remision" : {},
                # "motivo" : 1,
                # "tipoResponsable" : 1, 
                # "kms" : 150,
                # "fechaFactura" : "2022-08-21"
            # },
            "condicion" : {
                "tipo" : 1,
                "entregas" : [
                    { 
                        "tipo" : int(self.l10n_xma_payment_form_id.code),
                        "monto" : self.amount_total,
                        "moneda" : self.currency_id.name,
                        "cambio" : 0
                    }, 
                    # { 
                    #     "tipo" : 3,
                    #     "monto" : "150000",
                    #     "moneda" : "PYG",
                    #     "cambio" : 0,
                    #     "infoTarjeta" : {
                    #         "tipo" : 1,
                    #         "tipoDescripcion" : "Dinelco",
                    #         "titular" : "Marcos Jara",
                    #         "ruc" : "5448675-0",
                    #         "razonSocial" : "Bancard",
                    #         "medioPago" : 1,
                    #         "codigoAutorizacion" : 232524234
                    #     }
                    # }, 
                    # { 
                    #     "tipo" : 2,
                    #     "monto" : "150000",
                    #     "moneda" : "PYG",
                    #     "cambio" : 0,
                    #     "infoCheque" : {
                    #         "numeroCheque": "32323232",
                    #         "banco" : "Sudameris"
                    #     }
                    # }
                ],
                # "credito" : {
                #     "tipo" : 1,
                #     "plazo" : "30 días",
                #     "cuotas" : 2,
                #     "montoEntrega" : 1500000.00,
                #     "infoCuotas" : [
                #         {
                #             "moneda" : "PYG",
                #             "monto" : 800000.00,
                #             "vencimiento" : "2021-10-30"
                #         },
                #         {
                #             "moneda" : "PYG",
                #             "monto" : 800000.00,
                #             "vencimiento" : "2021-11-30"
                #         }
                #     ]
                # }
            },
            "items" : items,
            # "sectorEnergiaElectrica" : {
                # "numeroMedidor" : "132423424235425",
                # "codigoActividad" : 125,
                # "codigoCategoria" : "001",
                # "lecturaAnterior" : 4,
                # "lecturaActual" : 5
            # },# No esta en 
            # "sectorSeguros" : {
                # "codigoAseguradora" : "",
                # "codigoPoliza" : "AAAA",
                # "numeroPoliza" : "BBBB",
                # "vigencia" : 1,
                # "vigenciaUnidad" : "año",
                # "inicioVigencia" : "2023-03-01",
                # "finVigencia" : "2022-10-01",
                # "codigoInternoItem" : "A-001"
            # },
            # "sectorSupermercados" : {
                # "nombreCajero" : "Juan Antonio Caceres",
                # "efectivo" : 150000,
                # "vuelto" : 30000,
                # "donacion" : 1000,
                # "donacionDescripcion" : "Donado para la caridad"
            # },
            # "sectorAdicional" : {
                # "ciclo" : "Mensualidad",
                # "inicioCiclo" : "2023-02-01",
                # "finCiclo" : "2023-03-01",
                # "vencimientoPago" : "2023-03-07",
                # "numeroContrato" : "AF-2541",
                # "saldoAnterior" : 1550000
            # },
            # "detalleTransporte" : {
            #     "tipo" : 1,
            #     "modalidad" : 1,
            #     "tipoResponsable" : 1,
            #     "condicionNegociacion" : "CFR",
            #     "numeroManifiesto" : "AF-2541",
            #     "numeroDespachoImportacion" : "153223232332",
            #     "inicioEstimadoTranslado" : "2023-03-07",
            #     "finEstimadoTranslado" : "2023-03-07",
            #     "paisDestino" : "PRY", 
            #     "paisDestinoNombre" : "Paraguay",
            #     "salida" : {
            #         "direccion" : "Paraguay",
            #         "numeroCasa" : "Paraguay",
            #         "complementoDireccion1" : "Entre calle 2", 
            #         "complementoDireccion2" : "y Calle 7",
            #         "departamento" : 11,
            #         "departamentoDescripcion" : "ALTO PARANA",
            #         "distrito" : 143,
            #         "distritoDescripcion" : "DOMINGO MARTINEZ DE IRALA",
            #         "ciudad" : 3344,
            #         "ciudadDescripcion" : "PASO ITA (INDIGENA)",
            #         "pais" : "PRY",
            #         "paisDescripcion" : "Paraguay",
            #         "telefonoContacto" : "097x"
            #     },
            #     "entrega" : {
            #         "direccion" : "Paraguay",
            #         "numeroCasa" : "Paraguay",
            #         "complementoDireccion1" : "Entre calle 2", 
            #         "complementoDireccion2" : "y Calle 7",
            #         "departamento" : 11,
            #         "departamentoDescripcion" : "ALTO PARANA",
            #         "distrito" : 143,
            #         "distritoDescripcion" : "DOMINGO MARTINEZ DE IRALA",
            #         "ciudad" : 3344,
            #         "ciudadDescripcion" : "PASO ITA (INDIGENA)",
            #         "pais" : "PRY",
            #         "paisDescripcion" : "Paraguay",
            #         "telefonoContacto" : "097x"
            #     },
            #     "vehiculo" : {
            #         "tipo" : 1,
            #         "marca" : "Nissan",
            #         "documentoTipo" : 1, 
            #         "documentoNumero" : "232323-1",
            #         "obs" : "",
            #         "numeroMatricula" : "ALTO PARANA",
            #         "numeroVuelo" : 143
            #     },
            #     "transportista" : {
            #         "contribuyente" : true,
            #         "nombre" : "Paraguay",
            #         "ruc" : "80068684-1", 
            #         "documentoTipo" : 1,
            #         "documentoNumero" : "99714584",
            #         "direccion" : "y Calle 7",
            #         "obs" : 11,
            #         "pais" : "PRY",
            #         "paisDescripcion" : "Paraguay",
            #         "chofer" : {
            #             "documentoNumero" : "",
            #             "nombre" : "Jose Benitez",
            #             "direccion" : "Jose Benitez"
            #         },
            #         "agente" : {
            #             "nombre" : "Jose Benitez",
            #             "ruc" : "515415-1",
            #             "direccion" : "Jose Benitez"
            #         }
            #     }
            #},
            # "complementarios" : {
            #     "ordenCompra" : "",
            #     "ordenVenta" : "",
            #     "numeroAsiento" : "",
            #     "carga" : {
            #         "ordenCompra" : "",
            #         "ordenVenta" : "",
            #         "numeroAsiento" : ""
            #     }
            # },
            # "documentoAsociado" : {
            #     "formato" : 1,
            #     "cdc" : "01800695631001001000000612021112917595714694",
            #     "tipo" : 1,
            #     "timbrado" : "32323",
            #     "establecimiento" : "001",
            #     "punto" : "001",
            #     "numero" : "00278211",
            #     "fecha" : "2022-09-14",
            #     "numeroRetencion" : "32323232",
            #     "resolucionCreditoFiscal" : "32323",
            #     "constanciaTipo" : 1,
            #     "constanciaNumero" : 32323,
            #     "constanciaControl" : "33232323"
        }
        json_complete = {
            "id":self.id,
            "uuid_client":self.company_id.uuid_client,
            "params":json_params,
            "data": json_data,
            "rfc":'5448675',
            "prod": 'NO',
            "type": 'PF',
        }
        json_complete = self.delete_none_or_false(json_complete)
        json_complete = json.dumps(json_complete, default=str, separators=(',', ':'), ensure_ascii=True)

        res = str(json_complete)

        return res 
    
    def delete_none_or_false(self, _dict):
        if isinstance(_dict, dict):
            for key, value in list(_dict.items()):
                if isinstance(value, (list, dict, tuple, set)):
                    _dict[key] = self.delete_none_or_false(value)
                elif value is None or key is None:
                    del _dict[key]

        elif isinstance(_dict, (list, set, tuple)):
            _dict = type(_dict)(self.delete_none_or_false(item) for item in _dict if item is not None)

        return _dict

    
class AccountPayTerm(models.Model):
    _inherit = "account.payment.term"
    
    l10n_xma_payment_condition = fields.Selection([ ('1', 'plazo'),
                                                ('2', 'cuota'),],
                                               )
    
    l10n_xma_number = fields.Integer()




