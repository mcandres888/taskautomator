import json
import watson_developer_cloud


# this will be a helper class for ibm watson


class IBMWatson(object):
    WORKSPACE_ID = None
    WORKSPACE_URL = None
    WATSON_API_KEY = None
    WATSON_CRED_NAME = None
    WATSON_URL = None
    assistant = None

    def __init__(self):
        print "init"

    def initialize_from_config(self, config):
        print config
        self.WORKSPACE_ID = config.WORKSPACE_ID
        self.WORKSPACE_URL = config.WORKSPACE_URL
        self.WATSON_API_KEY = config.WATSON_API_KEY
        self.WATSON_CRED_NAME = config.WATSON_CRED_NAME
        self.WATSON_URL = config.WATSON_URL

        print self.WATSON_CRED_NAME

        #self.assistant = watson_developer_cloud.AssistantV1(
        #    username=self.WATSON_CRED_NAME,
        #    password=self.WATSON_API_KEY,
        #    version='2018-09-20'
        #)

        self.assistant = watson_developer_cloud.AssistantV1(
            url=self.WATSON_URL,
            iam_apikey=self.WATSON_API_KEY,
            version='2018-07-10'
        )


    def initialize_from_dict(self, config):
        print config
        self.WORKSPACE_ID = config['WORKSPACE_ID']
        self.WORKSPACE_URL = config['WORKSPACE_URL']
        self.WATSON_API_KEY = config['WATSON_API_KEY']
        self.WATSON_CRED_NAME = config['WATSON_CRED_NAME']
        self.WATSON_URL = config['WATSON_URL']

        print self.WATSON_CRED_NAME

        #self.assistant = watson_developer_cloud.AssistantV1(
        #    username=self.WATSON_CRED_NAME,
        #    password=self.WATSON_API_KEY,
        #    version='2018-09-20'
        #)

        self.assistant = watson_developer_cloud.AssistantV1(
            url=self.WATSON_URL,
            iam_apikey=self.WATSON_API_KEY,
            version='2018-07-10'
        )



###########################
#
# E N T I T I E S
#
###########################

    def getEntities(self, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
   
        response = self.assistant.list_entities(
            workspace_id = workspace_id
        ).get_result()

        print(json.dumps(response, indent=2))
        return response



    def createEntities(self, entity_name, values=None, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
   
        values_json = []

        if values is not None:
            for x in values:
                temp = {}
                temp['value'] = x
                values_json.append(temp)

        response = self.assistant.create_entity(
            workspace_id = workspace_id,
            entity = entity_name,
            values = values_json
        ).get_result()

        print(json.dumps(response, indent=2))
        return response


    def createEntitiesPattern(self, entity_name, values=None, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
   
        values_json = []

        if values is not None:
            for x in values:
                temp = {}
                temp['patterns'] = x
                temp['value'] = x
                temp['value_type'] = "patterns"
                values_json.append(temp)
        print "values json" , values_json

        response = self.assistant.create_entity(
            workspace_id = workspace_id,
            entity=entity_name,
            values=values_json
        ).get_result()

        print(json.dumps(response, indent=2))
        return response












###########################
#
# I N T E N T S
#
###########################



    def getIntents(self, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
   
        response = self.assistant.list_intents(
            workspace_id = workspace_id
        ).get_result()

        print(json.dumps(response, indent=2))
        return response


    def createIntents(self, intent_name, intent_desc, examples=None, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
        example_json = []

        if examples is not None:
            for x in examples:
                temp = {}
                temp['text'] = x
                example_json.append(temp)

        response = self.assistant.create_intent(
            workspace_id = workspace_id,
            intent=intent_name,
            description=intent_desc,
            examples=example_json
        ).get_result()

        print(json.dumps(response, indent=2))
        return response
     
     
###########################
#
# I N T E N T S - user inputs
#
###########################

     
      


    def getUserInputs(self, intents, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID

        userInputs = []
        for x in intents:
   
            response = self.assistant.list_examples(
                workspace_id = workspace_id,
                intent=x
            ).get_result()

            print(json.dumps(response, indent=2))
            userInputs.append(response)

        return response


 
###########################
#
# D I A L O G   N O D E S
#
###########################

    def getDialogNodes(self, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
   
        response = self.assistant.list_dialog_nodes(
            workspace_id = workspace_id
        ).get_result()

        print(json.dumps(response, indent=2))
        return response

    def deleteDialogNode(self, dialog_node, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
   
        response = self.assistant.delete_dialog_node(
            workspace_id = workspace_id,
            dialog_node = dialog_node
        ).get_result()

        print(json.dumps(response, indent=2))
        return response


    def deleteDialogNodeQuestionAnswer(self, dialog_node, workspace_id=None):
        self.deleteDialogNode( dialog_node, workspace_id)
        #self.deleteDialogNode( "%s_yes" % dialog_node, workspace_id)
        #self.deleteDialogNode( "%s_no" % dialog_node, workspace_id)





    def addEmailSlotForDialog(self, dialog_name , workspace_id=None):

        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID

        # add slots for email
        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            node_type = "slot",
            dialog_node = "%s_slot_email" % dialog_name,
            variable = "$email",
            parent = dialog_name
        ).get_result()
        print(json.dumps(response, indent=2))

        output = {}
        output['text'] = "Hi $person, Can I get your email?"
        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            node_type = "event_handler",
            dialog_node = "%s_handler_email" % dialog_name,
            event_name = "focus",
            parent = "%s_slot_email" % dialog_name,
            output = output
        ).get_result()
        print(json.dumps(response, indent=2))

        context = {}
        context['email'] = "@contactInfo"
        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            node_type = "event_handler",
            parent = "%s_slot_email" % dialog_name,
            context = context,
            conditions = "@contactInfo",
            event_name = "input",
            dialog_node = "%s_handler2_email" % dialog_name
        ).get_result()
        print(json.dumps(response, indent=2))


    def addPersonSlotForDialog(self, dialog_name , workspace_id=None):

        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID

        # add slots for email
        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            node_type = "slot",
            dialog_node = "%s_slot_person" % dialog_name,
            variable = "$person",
            parent = dialog_name
        ).get_result()
        print(json.dumps(response, indent=2))

        output = {}
        output['text'] = "Hi, can I get your name?"
        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            node_type = "event_handler",
            dialog_node = "%s_handler_person" % dialog_name,
            event_name = "focus",
            parent = "%s_slot_person" % dialog_name,
            output = output
        ).get_result()
        print(json.dumps(response, indent=2))

        context = {}
        context['person'] = "@sys-person"
        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            node_type = "event_handler",
            parent = "%s_slot_person" % dialog_name,
            context = context,
            conditions = "@sys-person",
            event_name = "input",
            dialog_node = "%s_handler2_person" % dialog_name
        ).get_result()
        print(json.dumps(response, indent=2))




    def createDialogQuestionAnswerCondition(self, dialog_name, dialog_title,  intent_condition, response, yes_answer, no_answer,  workspace_id=None): 
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
      
        output = {}
        output['generic'] = []
        output['generic'].append({"values":[{ "text" : response}],
                                  "response_type" : "text",
                                  "selection_policy": "sequential"})
        output['generic'].append({"description": "yes", 
                                  "response_type": "option",
                                  "title": "Reply yes or no",
                                  "options" : [
                                    { "value": { "input": { "text" : "yes"}},
                                      "label": "Yes"},
                                    { "value": { "input": { "text" : "no"}},
                                      "label": "No"}
                                   ]})


        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            dialog_node = dialog_name,
            conditions = intent_condition,
            output = output,
            node_type = "frame",
            title = dialog_title
        ).get_result()
        print(json.dumps(response, indent=2))


        # add email slot
        self.addEmailSlotForDialog(dialog_name )

        # add person slot
        self.addPersonSlotForDialog(dialog_name )

        # create the two conditions
        # yes
        output = {}
        output['text'] =  { "values" : [ yes_answer], 
                            "selection_policy": "sequential" }

        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            dialog_node = "%s_yes" % dialog_name,
            conditions = "@reply:yes",
            parent = dialog_name,
            output = output,
            node_type = "standard",
            title = "%s :yes" % dialog_title
        ).get_result()
        print(json.dumps(response, indent=2))

        # no
        output = {}
        output['text'] =  { "values" : [ no_answer], 
                            "selection_policy": "sequential" }

        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            dialog_node = "%s_no" % dialog_name,
            conditions = "@reply:no",
            parent = dialog_name,
            output = output,
            type = "standard",
            title = "%s :yes" % dialog_title
        ).get_result()
        print(json.dumps(response, indent=2))


        return response


    def createDialogQuestionAnswerPlain(self, dialog_name, dialog_title,  intent_condition, answer, workspace_id=None): 
        if workspace_id is None:
            workspace_id = self.WORKSPACE_ID
      
        output = {}
        output['generic'] = []
        output['generic'].append({"values":[{ "text" : answer}],
                                  "response_type" : "text",
                                  "selection_policy": "sequential"})

        response = self.assistant.create_dialog_node(
            workspace_id = workspace_id,
            dialog_node = dialog_name,
            conditions = intent_condition,
            output = output,
            node_type = "frame",
            title = dialog_title
        ).get_result()
        print(json.dumps(response, indent=2))

        # add email slot
        self.addEmailSlotForDialog(dialog_name )

        # add person slot
        self.addPersonSlotForDialog(dialog_name )



        return response



