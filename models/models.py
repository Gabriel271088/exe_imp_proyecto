# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _


class Course(models.Model):
    _name = 'imports.folder'
    _description = "OpenAcademy Courses"

    name = fields.Char(required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users', string='Responsible', ondelete='set null', index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    name_folder = fields.Char(string='Nombre de la tarea')
    partner_folder = fields.Many2one('res.partner', string='Cliente')
    category_folder = fields.Many2one(string='Categorias')
    importacion = fields.Boolean(string='Importacion')
    user_folder = fields.Many2one('res.users', string='Responsable de proyecto')
    planned_date_folder = fields.Datetime(string='Fecha planificada')
    company_folder = fields.Many2one('res.company',string='Compañia')

    description_folder = fields.Text()
    ajustes_folder = fields.Text()
    items_folder = fields.Text()

    state_folder = fields.Selection([
        ('new', 'NUEVO'),
        ('to do', 'POR HACER'),
        ('In process', 'EN PROCESO'),
        ('blocked', 'BLOQUEADA'),
        ('finalized', 'FINALIZADA'),], string='Form States',
        copy=False, default='new', required=True)    

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]



class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"
    
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    course_id = fields.Many2one('imports.folder', string='Proyectos', ondelete='cascade', required=True)
    user_id = fields.Many2one('res.users', string='Asignados')
    supplier = fields.Many2one('res.partner', string='Proveedor')
    instructor_id = fields.Many2one('res.partner', string='Agente de carga')
    dispatch = fields.Integer(string='Despacho')
    import_license = fields.Char(string='Licencia de importación')
    ncm = fields.Char(string='NCM')
    incoterm = fields.Char(string='INCOTERM')
    total_mercaderia = fields.Float(string='Total mercadería')
    total_gastos = fields.Float(string='Total gastos')
    coeff_real = fields.Float(string='Coeficiente real')
    final_value = fields.Float(string='Valor final')
    #attendee_ids = fields.Many2many('res.partner', string="Attendees")
    active = fields.Boolean(default=True)

    description = fields.Text()
    sub_tarea = fields.Text()
    detalle_carga = fields.Text()
    fechas = fields.Text()
    costos = fields.Text()

    partner = fields.Many2one('res.partner', string='Cliente')
    planned_date = fields.Datetime(string='Fecha planificada')
    date_deadline = fields.Date(string='Fecha limite')
    category = fields.Many2one(string='Categorias')
    etd = fields.Date(string='ETD')
    eta = fields.Date(string='ETA')
    closing_date = fields.Date(string='Fecha de cierre de importación')
    needs = fields.Boolean(string='Requiere refacturación a ASCAM ',default=False)
    days_folder = fields.Integer(string='Total días de duración de carpeta')



    #taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')

    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)

    account_move_count = fields.Integer()
    purchase_order_count = fields.Integer()
    stock_picking_count  = fields.Integer()  
    color = fields.Integer()

    shipping = fields.Selection([
        ('mar','Marítimo'),
        ('air','Aéreo'),
        ('ground','Terrestre'),
    ],default=False,string='')

    currency = fields.Selection([
        ('usd','USD'),
        ('eur','EUR'),
        ('gbp','GBP'),
    ],default=False,string='Divisa')

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
    ], default='0', index=True,)

    kanban_state = fields.Selection([ ('normal', 'Grey'), ('done', 'Green'), ('blocked', 'Red')], string='Kanban State',
    copy=False, default='normal', required=True)
    
    kanban_states = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')], string='Kanban State',
        copy=False, default='normal', required=True)

    states = fields.Selection([
        ('new', 'NUEVO'),
        ('to do', 'POR HACER'),
        ('In process', 'EN PROCESO'),
        ('blocked', 'BLOQUEADA'),
        ('finalized', 'FINALIZADA'),], string='Kanban State',
        copy=False, default='new', required=True)
    
    statistics = fields.Date(string='Creación de estadística')
    order_sent = fields.Date(string='Pedido enviado al proveedor')
    supp_invoice = fields.Date(string='Factura del proveedor')
    supp_list = fields.Date(string='Lista del proveedor')
    arrived = fields.Date(string='Arribo en la empresa')
    reception_in_logistics = fields.Date('Recepción en Logística')
    payment_mulc = fields.Date(string='Pago por MULC')
    date_dispatch = fields.Date(string='Fecha de despacho')

    estimated_founds = fields.Float(string='Fondos estimados de aduana')
    expense = fields.Float(string='Gastos FFWW')
    dispatch_import = fields.Float(string='Despacho de importación')

    coste_currency = fields.Selection([
        ('usd','USD'),
        ('eur','EUR'),
    ],default=False,string='Moneda')

   # @api.depends('seats', 'attendee_ids')
    #def _taken_seats(self):
        #for r in self:
            #if not r.seats:
                #r.taken_seats = 0.0
            #else:
                #r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    #@api.onchange('seats', 'attendee_ids')
    #def _verify_valid_seats(self):
       # if self.seats < 0:
            #return {
                #'warning': {
                    #'title': _("Incorrect 'seats' value"),
                   # 'message': _("The number of available seats may not be negative"),
               # },
           # }
        #if self.seats < len(self.attendee_ids):
            #return {
                #'warning': {
                    #'title': "Too many attendees",
                    #'message': "Increase seats or remove excess attendees",
                #},
           # }

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1

    #@api.depends('attendee_ids')
    #def _get_attendees_count(self):
        #for r in self:
           # r.attendees_count = len(r.attendee_ids)

   # @api.constrains('instructor_id', 'attendee_ids')
    #def _check_instructor_not_in_attendees(self):
       # for r in self:
            #if r.instructor_id and r.instructor_id in r.attendee_ids:
               # raise exceptions.ValidationError("A session's instructor can't be an attendee")


