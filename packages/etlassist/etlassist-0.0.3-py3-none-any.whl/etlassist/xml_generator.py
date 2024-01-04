from lxml import etree

# modify function to be developed further for customization of data inputs
def modify(data,func_name):
  if func_name == "string":
    return data

# appender helps in building the xml as per the config
def _appender( config , data , tag , base_value ):
  
  global depth_tag 
  looper = False
  
  empty_flag = False
  
  temp = ""
  
  if(config['type'] == 'refer' or config['type'] == 'iterate'):
    if config["value"] == "":
      temp = base_value
    elif config["value"] == "CARRYFORWARD":
      temp = data
    elif('.' in config["value"]):
      temp = data
      try:
        for idx in config['value'].split("."):
          if type(temp) == list:
            temp = temp[0]
          temp = temp[idx]
      except Exception as e:
          temp = ""
    else:
      temp = data[config["value"]]
      
    
  
  if(config['type'] == 'base'):
    if('.' in config["value"]):
      temp = base_value
      for idx in config['value'].split("."):
        temp = temp[idx]
    elif config["value"] == "":
      temp = base_value
    else:
      temp = base_value[config["value"]]
    
  
  if((temp == None or temp == "None" or temp == "")):
    empty_flag = True
  
  if( empty_flag and config['mandatory'] == "1" and config["type"] != "default"):
      raise Exception({"exception_code" : "TAG_MISSING" , "exception_message" : "Tag missing " + config['value'] })
  
  def create_tag(tag,sub_tag):
    if("." in sub_tag):
      root = tag
      elems = sub_tag.split(".")
      if("CustomFieldList.CustomField.Value" in sub_tag):
          root = depth_tag["looper_tag"]
      else:
        for i in range(len(elems)-1):
          if i != 0 :
            parent = elems[i-1]
          else:
            parent = "base"
          if(parent+"_"+elems[i] in depth_tag.keys()):
            root = depth_tag[parent+"_"+elems[i]]
          else:
            root = etree.SubElement(root, elems[i])
            if(elems[i] == "CustomField"):
              depth_tag["looper_tag"] = root
            else:
              depth_tag[parent+"_"+elems[i]] = root
              
      return root , elems[-1]
    else:
      return tag , sub_tag
  
  if(empty_flag and config['type'] != 'default'):
    mod_tag,sub_tag = create_tag(tag,config['identifier'])
    etree.SubElement( mod_tag , sub_tag ).text = ""
    
  elif config['type'] == 'refer' :
    mod_tag,sub_tag = create_tag(tag,config['identifier'])
    etree.SubElement( mod_tag , sub_tag ).text = (modify(str(temp), config['property']))
  
  elif config['type'] == 'default' :
    mod_tag,sub_tag = create_tag(tag,config['identifier'])
    etree.SubElement( mod_tag , sub_tag ).text = (modify(str(config["value"]), config['property']))
  
  elif config['type'] == "base":
    mod_tag,sub_tag = create_tag(tag,config['identifier'])
    etree.SubElement( mod_tag , sub_tag ).text = (modify(str(temp), config['property']))
  
  elif config['type'] == "iterate":    
    loop_flag = False
    if(isinstance(temp, list)): 
      loop_flag = True
    
    if(loop_flag):
      for detail in temp:
        if("." not in config['identifier']):
          inner_tag = etree.SubElement(tag, config['identifier'])
          for inval in config["config"]:
            _appender(inval,detail,inner_tag,base_value)
        else:
          mod_tag,sub_tag = create_tag(tag,config['identifier'])
          inner_tag = etree.SubElement( mod_tag , sub_tag )
          for inval in config["config"]:
            _appender(inval,detail,inner_tag,base_value)
    else:
      inner_tag = etree.SubElement(tag, config['identifier'])
      for inval in config["config"]:
        _appender(inval,temp,inner_tag,base_value)
  

# main function to be used for the cml creation
def create_xml(config,data,tags):
  
  try: 
    
    global depth_tag

    depth_tag = {

    }
    
    base_value = data

    if('namespaces' in tags.keys()):
      root = etree.Element(tags['root'] ,{etree.QName(tags['attr_qname'][0],tags['attr_qname'][1]) : tags['attr_qname_val']}, nsmap = tags['namespaces'] )
    else:
      root = etree.Element(tags['root'])

    if 'sub_root' in tags.keys():
      sub = etree.SubElement(root, tags['sub_root'])
      for val in config:
        _appender(val,data,sub,base_value)
    else:
      for val in config:
        _appender(val,data,root,base_value)

    return etree.tostring(root, pretty_print=True).decode("utf-8")
  
  except Exception as e:
    return str(e)

