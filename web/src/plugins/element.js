import Vue from 'vue'
import {
  Button,
  Form,
  FormItem,
  Input,
  Message,
  Container,
  Header,
  Aside,
  Main,
  Menu,
  Submenu,
  MenuItem,
  Breadcrumb,
  BreadcrumbItem,
  Card,
  Row,
  Col,
  Table,
  TableColumn,
  Tooltip,
  Pagination,
  Dialog,
  MessageBox,
  Carousel,
  CarouselItem,
  Avatar,
  Select,
  Option,
  Steps,
  Step,
  Tabs,
  TabPane,
  Upload,
  Loading,
	Tag,
	Link,
	Divider,
	Progress,
	Rate,

  } from 'element-ui'

Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Tooltip)
Vue.use(Pagination)
Vue.use(Dialog)
Vue.use(Carousel)
Vue.use(CarouselItem)
Vue.use(Avatar)
Vue.use(Select)
Vue.use(Option)
Vue.use(Steps)
Vue.use(Step)
Vue.use(Tabs)
Vue.use(TabPane)
Vue.use(Upload)
Vue.use(Tag)
Vue.use(Link)
Vue.use(Divider)
Vue.use(Progress)
Vue.use(Rate)


Vue.prototype.$loading = Loading.service;
Vue.prototype.$message = Message
Vue.prototype.$msgbox = MessageBox
Vue.prototype.$alert = MessageBox.alert
Vue.prototype.$confirm = MessageBox.confirm
Vue.prototype.$prompt = MessageBox.prompt
