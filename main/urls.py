from django.urls import path
from django.shortcuts import render, redirect, reverse

from . import views
from utils.ec2 import test

urlpatterns = [
     path('', views.index, name="index"),
     path('user_dashboard', views.user_dashboard, name="user_dashboard" ),
     path('user_dashboard/user_action_form/instance', views.user_action_form, name="user_action_form" ),
     path('user_dashboard/update_usage', views.update_usage, name="update_usage" ),
     path('stop/instance', views.stop, name="stop" ),
     path('update_user/<int:pk>', views.update_password, name="update_password" ),
     path('update_password_superuser/<int:pk>', views.update_password_superuser, name="update_password_superuser" ),
     path('update_time/instance', views.update_time, name="update_time" ),
     path('superuser_dashboard', views.superuser_dashboard, name="superuser_dashboard" ),
     path('user_home', views.superuser_home, name="superuser_home" ),
     path('control_panel', views.control_panel, name="control_panel" ),
     path('control_panel_vps', views.control_panel_vps, name="control_panel_vps" ),
     path('control_panel_proxy', views.control_panel_proxy, name="control_panel_proxy" ),
     path('manual_proxy_add_control_panel_proxy', views.manual_proxy_add_control_panel_proxy, name="manual_proxy_add_control_panel_proxy" ),
    
    
     path('user_accounts', views.user_accounts, name="user_accounts" ),
     path('superuser_accounts', views.superuser_accounts, name="superuser_accounts" ),
     
     path('vps_view_summary_control_panel', views.vps_view_summary_control_panel, name="vps_view_summary_control_panel" ),
     path('vps_manual_control_panel', views.vps_manual_control_panel, name="vps_manual_control_panel" ),

     
     path('proxy_view_summary', views.proxy_view_summary, name="proxy_view_summary" ),
     path('manual_proxy', views.manual_proxy, name="manual_proxy" ),
     path('upload_csv', views.upload_csv, name="upload_csv" ),
    
    
     path('control_panel_vpn', views.control_panel_vpn, name="control_panel_vpn" ),
     path('vpn_view_summary', views.vpn_view_summary, name="vpn_view_summary" ),
     path('manual_vpn', views.manual_vpn, name="manual_vpn" ),
     path('edit_manual_vpn/<int:pk>', views.edit_manual_vpn, name="edit_manual_vpn" ),
     
     path('upload_vpn_csv', views.upload_vpn_csv, name="upload_vpn_csv" ),

     path('packages', views.packages, name="buy_now"),
    
     path('buy/<int:pk>', views.buy, name="buy"),

     path('create_instance', views.create_instance__u, name="create_instance" ),
     path('vps_history_spu', views.vps_history_spu, name="vps_history_spu" ),
     path('vpn_history_spu', views.vpn_history_spu, name="vpn_history_spu" ),
     path('proxies_history_spu', views.proxies_history_spu, name="proxies_history_spu" ),
     path('superuser_add_vpn', views.superuser_add_vpn, name="superuser_add_vpn" ),

     path('sell_template_to_sellers', views.sell_template_to_sellers, name="sell_template_to_sellers"),
     path('add_sell_template_to_sellers', views.add_sell_template_to_sellers, name="add_sell_template_to_sellers"),
     path('edit_sell_template_to_sellers/<int:pk>', views.edit_sell_template_to_sellers, name="edit_sell_template_to_sellers"),
     path('delete_sell_template_to_sellers/<int:pk>', views.delete_sell_template_to_sellers, name="delete_sell_template_to_sellers"),
     path('add_templates_to_sellers/<int:pk>', views.add_templates_to_sellers, name="add_templates_to_sellers"),
     path('update_seller_info/<int:pk>/<int:id>', views.update_seller_info, name="update_seller_info"),
     path('admin_sell_template_to_sellers', views.admin_sell_templates_to_sellers, name='admin_sell_templates_to_sellers'),
     path('admin_delete_template/<int:pk>', views.admin_delete_template, name='admin_delete_template'),


     path('seller', views.seller, name="seller" ),
     path('add_seller', views.add_seller, name="add_seller" ),

     path('add_credit', views.add_credit, name="add_credit" ),
     path('add_seller_credit', views.add_seller_credit, name="add_seller_credit" ),

     path('superuser_add_proxy', views.superuser_add_proxy, name="superuser_add_proxy" ),
     path('superuser_add_vps', views.superuser_add_vps, name="superuser_add_vps" ),
     path('templates', views.templates, name="templates" ),
     path('templates/add', views.templates_add, name="templates_add" ),
     path('templates/edit/<int:pk>', views.templates_edit, name="templates_edit" ),
     path('templates/delete/<int:pk>', views.templates_delete, name="templates_delete" ),
     path('instances/generate/<int:pk>', views.generate_instance, name="generate_instance" ),
     path('generate_seller_instance_superuser/generate/<int:pk>', views.generate_seller_instance_superuser, name="generate_seller_instance_superuser" ),
     path('instances/seller_generate_instance/<int:pk>', views.seller_generate_instance, name="seller_generate_instance" ),
     path('instances/attach_user/<int:pk>', views.superuser_attach_user, name="superuser_attach_user" ),
     path('instances/details/<int:pk>', views.instance_details, name="instance_details" ),
     path('aws_accounts', views.aws_accounts, name="aws_accounts" ),
     path('aws_account/add', views.aws_account_add, name="aws_account_add" ),
     path('aws_account/edit/<int:pk>', views.aws_account_edit, name="aws_account_edit" ),
     path('instance/renew/<int:pk>', views.instance_renew, name="instance_renew" ),
     path('instance/terminate/<int:pk>', views.instance_terminate, name="instance_terminate" ),
     path('instance/update_time/<int:pk>/<int:page>', views.update_time, name="update_time" ),
     path('control_panel_vps/renew/<int:pk>', views.admin_renew, name="admin_renew" ),
     path('contro_panel_vps/terminate/<int:pk>', views.admin_terminate, name="admin_terminate" ),
     path('control_panel_vps/renew/<int:pk>', views.admin_renew, name="superuser_renew" ),
     path('contro_panel_vps/terminate/<int:pk>', views.admin_terminate, name="superuser_terminate" ),
     path('control_panel_proxy/terminate/<int:pk>', views.proxy_terminate, name="proxy_terminate" ),
     path('delete_instance/<int:pk>/<int:page>', views.delete_vps, name="delete_vps" ),
     path('delete_user/<int:pk>', views.delete_user, name="delete_user" ),
     path('delete_user_accounts/<int:pk>', views.delete_user_accounts, name="delete_user_accounts" ),

     path('account/<int:pk>', views.account, name="account" ),
     path('usage/<int:pk>', views.usage, name="usage" ),
     path('usage/delete/<int:pk>', views.usage_delete, name="usage_delete" ),
     path('make_payment', views.make_payment, name="make_payment" ),
     path('test', views.quick_terminate),
     path('contact-us', views.contactUs, name="contactUs" ),
     path('proxy_details/<int:pk>', views.proxy_details, name="proxy_user" ),
     path('download_rdp/<int:pk>', views.download_rdp, name="download_rdp" ),
     path('upload_csv', views.upload_csv, name="upload_csv" ),
     path('delete_csv/<int:pk>', views.delete_file, name="delete_file"),
     
     path('instances/gen/<int:pk>', views.GEN_REA, name="generate_instance" ),

]
