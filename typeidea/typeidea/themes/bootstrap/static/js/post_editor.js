(function($){
	var $content_md = $('#div_id_content_md');
	var $content_ck = $('#div_id_content_ck');
	var $is_md = $('input[name = is_md]');
	var switch_editor = function(is_md){
		if(is_md) {
			$content_md.show();
			$content_ck.hide();
		} else {
			$content_md.hide();
			$content_ck.show();
		}
	}
	$is_md.on('click',function() {
		//每当用户在页面中 选择/取消勾选Markdown语法 的时候就会触发这个函数，显示不同的正文编辑框。
		//用户可以在相应的盒子中输入正文的内容，在后端的modelform的自定义子类中会使用自定义的clean方法把干净的数据
		//保存在cleaned_data中
		switch_editor($(this).is(':checked'));
	});
	switch_editor($is_md.is(':checked'));
})(jQuery);
