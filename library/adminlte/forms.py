# base class for controllers
from flask import Markup


class Forms:
    # this object is responsible or creating forms inside the template

    # form data example
    '''
    header = {
        "action" : "",
        "method" : "",
        "enctype" : ""
    }
    data = [
        {'type' : 'text', 'name' : 'stall_code', 'place_holder' : 'Stall Code', 'label' : 'Stall Code'},
        {'type' : 'select', 'name' : 'stall_code', 'label' : 'Stall Code', 'options' : [ { 'value' : "0" , 'label' : "Disabled" , 'selected' : False}]},

    ]
    '''

    @staticmethod
    def createForm(header, data, btn_footer):

        html_str = "<form role='form' action='%s' method='%s' enctype='%s'>" % (header['action'], header['method'], header['enctype'])
        html_str += "<div class='box-body'>"


        for d in data:
            if 'type' not in d:
                print "error"
                # need type
                continue

            if d['type'] == "text":
                html_str += Forms.type_text(d)
            elif d['type'] == "select":
                html_str += Forms.type_select(d)
            elif d['type'] == "hidden":
                html_str += Forms.type_hidden(d)

        html_str += Forms.btn_submit(btn_footer)
        html_str += "</div></form>"
        return Markup(html_str)


    @staticmethod
    def createFormDisplayOnly(data):

        html_str = "<div class='box-body'>"
        for d in data:
            if 'type' not in d:
                print "error"
                # need type
                continue
            if d['type'] == "text":
                html_str += Forms.type_text(d)
            elif d['type'] == "select":
                html_str += Forms.type_select(d)
            elif d['type'] == "hidden":
                html_str += Forms.type_hidden(d)

        html_str += "</div>"
        return Markup(html_str)


    @staticmethod
    def create_add_content (json_data):
        html_str = "<div class='box-footer'>"
        for x in json_data:
            onclick_str = "location.href=\"%s\";" % x['url']
            html_str += "<button onclick='%s' class='btn %s'>%s</button>&nbsp&nbsp&nbsp" % (onclick_str, x['class'], x['title'])
        html_str += "</div>" 
        return Markup(html_str)




    @staticmethod
    def btn_submit(btn_footer):
        html_str = "<div class='box-footer'>"
        html_str += "<button type='submit' class='btn btn-primary'>%s</button></div>" % btn_footer
        return html_str

    @staticmethod
    def type_hidden(d):
        html_str = "<input type='hidden' id='%s' name='%s' value='%s'>" % (d['name'], d['name'], d['value'])
        return html_str

    #    {'type' : 'text', 'name' : 'stall_code', 'place_holder' : 'Stall Code', 'label' : 'Stall Code'},
    @staticmethod
    def type_text(d):
        html_str = "<div class='form-group'>"
        html_str += "<label for='%s'>%s</label>" % (d['name'], d['label'])
        html_str += "<input type='text' class='form-control' id='%s' name='%s' placeholder='%s' value='%s'>" % (d['name'], d['name'],d['label'], ('value' in d and d['value'] or ''))
        html_str += "</div>"

        return html_str
    #{'type' : 'select', 'name' : 'stall_code', 'label' : 'Stall Code', 'options' : [ { 'value' : "0" , 'label' : "Disabled" , 'selected' : False}]},

    @staticmethod
    def type_select (d):
        html_str = "<div class='form-group'>"
        html_str += "<label for='%s'>%s</label>" % (d['name'], d['label'])
        html_str += "<select class='form-control' id='%s' name='%s' >" % (d['name'], d['name'])
        for x in d['options']:
            if 'selected' in x and x['selected']  :
                html_str += "<option value='%s' selected>%s</option>" % (x['value'], x['label'])
            else:
                html_str += "<option value='%s'>%s</option>" % (x['value'], x['label'])

        html_str += "</select></div>"

        return html_str
