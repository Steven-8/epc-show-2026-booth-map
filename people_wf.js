export const meta = {
  name: 'epc-key-personnel',
  description: 'Find named public business contacts for 15 key EPC Show 2026 exhibitors (turbine/power/EPC)',
  phases: [{ title: 'People', detail: 'one agent per key company' }],
}
const HL = [{"slug": "siemens-energy", "name": "Siemens Energy", "stand": "A16", "zone": "A", "cat": "燃机/发电", "note": "燃气轮机与发电系统全球巨头，航改燃机直接同业"}, {"slug": "baker-hughes", "name": "Baker Hughes", "stand": "G6", "zone": "G", "cat": "燃机/旋转设备", "note": "NovaLT 燃气轮机与压缩机驱动，旋转设备核心供应商"}, {"slug": "gulf-turbine-services", "name": "Gulf Turbine Services", "stand": "Q31", "zone": "Q", "cat": "燃机服务", "note": "燃气轮机维修与服务，航改机组运维相关"}, {"slug": "turbine-x", "name": "Turbine X", "stand": "K11", "zone": "K", "cat": "燃机", "note": "燃气轮机相关业务"}, {"slug": "kobelco-compressors-america-inc", "name": "Kobelco Compressors America, Inc.", "stand": "F31", "zone": "F", "cat": "旋转设备", "note": "离心/螺杆压缩机，燃机驱动配套"}, {"slug": "cummins", "name": "Cummins", "stand": "N3", "zone": "N", "cat": "发电机组", "note": "柴油/燃气发电机组与动力系统"}, {"slug": "aggreko", "name": "Aggreko", "stand": "Q32", "zone": "Q", "cat": "临时发电", "note": "移动式发电与温控租赁，分布式电力同业"}, {"slug": "abb", "name": "ABB", "stand": "Q17", "zone": "Q", "cat": "电气/自动化", "note": "电气化、自动化与驱动，电站配套"}, {"slug": "saber-power", "name": "Saber Power", "stand": "M17", "zone": "M", "cat": "电力系统", "note": "电力工程与配电系统"}, {"slug": "sieyuan-electric-usa", "name": "Sieyuan ELectric USA", "stand": "B34", "zone": "B", "cat": "电力设备", "note": "输配电与电力设备"}, {"slug": "distributed-power-solutions", "name": "Distributed Power Solutions", "stand": "F24", "zone": "F", "cat": "分布式发电", "note": "分布式天然气发电方案，直接同业"}, {"slug": "transtech-energy", "name": "TransTech Energy", "stand": "N11", "zone": "N", "cat": "天然气/发电", "note": "天然气处理与能源系统"}, {"slug": "air-liquide-engineering-construction", "name": "Air Liquide Engineering & Construction", "stand": "A7", "zone": "A", "cat": "大型EPC", "note": "气体处理与能源工程总包(EPC)"}, {"slug": "powergen-controls", "name": "Powergen Controls", "stand": "R42", "zone": "R", "cat": "发电控制", "note": "发电机组控制系统"}, {"slug": "buffalo-pumps", "name": "Buffalo Pumps", "stand": "C40", "zone": "C", "cat": "旋转设备", "note": "离心泵，电站/油气配套旋转设备"}];
const SCHEMA = { type:'object', additionalProperties:false, required:['slug','people','note'],
  properties:{
    slug:{type:'string'},
    note:{type:'string', description:'若找不到具名联系人，用一句话说明（中文）'},
    people:{ type:'array', description:'公开可得的具名商务联系人(0-3名)', items:{
      type:'object', additionalProperties:false, required:['name','title','email','kind'],
      properties:{
        name:{type:'string', description:'姓名'},
        title:{type:'string', description:'职务(中文或英文皆可)'},
        email:{type:'string', description:'公开邮箱；无则留空'},
        kind:{type:'string', enum:['verified_public','official_general','linkedin','inferred','unknown']}
      }}}
  }}
phase('People')
const out = await parallel(HL.map(h=>()=>
  agent(
    `请为美国 EPC Show 2026(休斯敦油气/电力/工程展会)的参展商「${h.name}」(展位 ${h.stand})查找【公开可得】的具名商务对接人，用于展位可视化的"参展人员"信息。\n`+
    `优先：公司官网 team/leadership/sales/business development 页面、新闻稿、公开 LinkedIn 上列出的 销售/业务发展/市场/区域经理 等。\n`+
    `严格要求：只用公开来源，可给 0-3 人；查不到具名个人就返回空 people 并在 note 说明(例如"官网未公开具名销售联系人，建议经 info@ 对接")。【绝对不要编造】姓名或邮箱；不确定的邮箱 kind 标 inferred 或 unknown；LinkedIn 个人页填进 email 字段并把 kind 标 linkedin。\n`+
    `注意：这是公开商务联系人，未必是实际到场展位人员——这点没关系，找公开商务对接人即可。返回 slug=${JSON.stringify(h.slug)}。`,
    { label:h.name, schema:SCHEMA, agentType:'general-purpose' }
  ).catch(()=>({slug:h.slug,people:[],note:'检索失败'}))
))
return out
