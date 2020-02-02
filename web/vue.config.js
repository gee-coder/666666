module.exports = {
  //解决打包后一片空白的问题
  publicPath: './',
  //改相对路径别名的配置
	configureWebpack: {
		resolve: {
			alias: {
				'assets': '@/assets',
				'img': 'assets/img',
				'css': 'assets/css',
				'components': '@/components',
				'common': 'components/common',
				'content': 'components/content',
				'network': '@/network',
				'store': '@/store',
			}
		}
	}
}
