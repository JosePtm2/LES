from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import  Process, Activity, Role, Product
from Users.models import User, Organization
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Users.forms import NewUserForm
from Activities.models import Pattern
from Activities.views import AjaxableResponseMixin
from .forms import  SwapActivityForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django import forms




@login_required(login_url='/login')
def processos(request):
	return render(request=request,
				  template_name="processes/processos.html",
				   context={"procs": Process.objects.filter(user__organization=request.user.organization), "acts": Activity.objects.all()})


@login_required(login_url='/login')
def actividades(request):
	return render(request=request,
				  template_name="processes/actividades.html",
				   context={"acts": Activity.objects.all().exclude(original__isnull=False), "proc_acts": Activity.objects.filter(process__user=request.user)})

@login_required(login_url='/login')
def removeActivityFromProcess(request, **kwargs):
	this_act = Activity.objects.filter(pk=kwargs['pk'])[0]
	messages.warning(request,f"Actividade \""+ this_act.activity_name+ f"\" apagada do sistema")
	this_act.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))#previous URL


class ActivityCreate(CreateView):
	model = Activity
	fields = ['activity_name', 'description', 'pattern', 'role'] 
	template_name = "processes/forms/activity_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(ActivityCreate, self).get_form(form_class)
		#form.fields['user'].widget
		form.fields['pattern'] = forms.ModelMultipleChoiceField(queryset=Pattern.objects.all() ,widget=forms.CheckboxSelectMultiple(), required=False)
		form.fields['role'] = forms.ModelMultipleChoiceField(queryset=Role.objects.all() ,widget=forms.CheckboxSelectMultiple(),required=False)
		form.fields['activity_name'].label = "Nome da actividade"
		form.fields['description'].label = "Descrição"
		form.fields['pattern'].label = "Padrões"
		form.fields['role'].label = "Papéis"
		return form	

	def form_valid(self, form):
		messages.info(self.request, f"Actividade " +  " \""+ form.cleaned_data['activity_name'] + f"\" inserida no sistema")
		return super(ActivityCreate, self).form_valid(form)

class ActivityDetail(DetailView):
	model = Activity
	template_name = "processes/forms/activity_detail.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		act_id = self.object.id
		context['pid'] = self.kwargs['pk']
		our_products = Product.objects.all().filter(activity__id=act_id)
		this_act = Activity.objects.all().filter(id=act_id)[0]
		our_roles = this_act.role.all()
		our_patterns = this_act.pattern.all()
		context['act_products'] = our_products
		context['non_products'] = Product.objects.all().exclude(id__in=our_products)
		context['patterns'] = our_patterns
		context['non_patterns'] = Pattern.objects.all().exclude(id__in=our_patterns)
		context['roles'] = our_roles
		context['non_roles'] = Role.objects.all().exclude(id__in=our_roles)
		context['procs'] = Process.objects.all()
		return context

class ActivityUpdate(UpdateView):
	model = Activity
	fields = ['activity_name', 'description', 'pattern', 'role'] 
	template_name = "processes/forms/activity_update_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(ActivityUpdate, self).get_form(form_class)
		#form.fields['user'].widget
		form.fields['role'] = forms.ModelMultipleChoiceField(queryset=Role.objects.all() ,widget=forms.CheckboxSelectMultiple(), required=False)
		form.fields['pattern'] = forms.ModelMultipleChoiceField(queryset=Pattern.objects.all() ,widget=forms.CheckboxSelectMultiple(), required=False)
		form.fields['activity_name'].label = "Nome da actividade"
		form.fields['description'].label = "Descrição"
		form.fields['pattern'].label = "Padrões"
		form.fields['role'].label = "Papéis"
		return form		

	def form_valid(self, form):
		messages.info(self.request, f"Actividade " +  " \""+ form.cleaned_data['activity_name'] + f"\" alterada com sucesso")
		return super(ActivityUpdate, self).form_valid(form)

class ActivityDelete(DeleteView):
	model = Activity
	template_name = "processes/forms/activity_confirm_delete.html"
	def get_context_data(self, **kwargs):
		context = super(ActivityDelete, self).get_context_data(**kwargs)
		this_acts = Activity.objects.filter(original=self.kwargs['pk'])
		context['act_procs'] = this_acts
		return context

	def delete(self, request, *args, **kwargs):
		messages.warning(self.request,f"Actividade " +  " \""+ Activity.objects.filter(id=self.kwargs['pk'])[0].activity_name+ f"\" apagada do sistema")
		return super(ActivityDelete, self).delete(request, *args, **kwargs)

class ActivitySwap(CreateView):
	model = Activity
	sucess_url = "/actividades"
	template_name = "processes/forms/activity_update_form.html"
	fields = ['activity_name', 'description', 'role', 'pattern', 'process', 'original']
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(ActivitySwap, self).get_form(form_class)
		this_act = Activity.objects.filter(pk =self.kwargs['pk'])[0]
		this_proc = Process.objects.filter(pk =self.kwargs['fk'])[0]
		form.fields['activity_name'].widget = forms.TextInput(attrs={'value': this_act.activity_name})
		form.fields['description'].widget = forms.TextInput(attrs={'value': this_act.description})
		all_roles = Role.objects.all()
		original_choice = Activity.objects.filter(pk =self.kwargs['pk'])
		form.fields['pattern'] = forms.ModelMultipleChoiceField(queryset=Pattern.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
		form.fields['role'] = forms.ModelMultipleChoiceField(queryset=all_roles, widget=forms.CheckboxSelectMultiple(), required=False)
		form.fields['original'] = forms.ModelChoiceField(queryset=original_choice, widget=forms.RadioSelect())
		form.fields['original'].empty_label = None
		form.fields['process'].empty_label = None
		roles = Role.objects.filter(pk__in = this_act.role.all())
		patterns = Pattern.objects.filter(pk__in = this_act.pattern.all())
		form.initial['role'] = roles
		form.initial['process'] = this_proc
		form.initial['pattern'] = patterns
		form.initial['original'] = this_act.id
		return form

	def form_valid(self, form):
		messages.info(self.request, f"Actividade " +  " \""+ form.cleaned_data['activity_name'] + f"\" associada ao processo \" " + form.cleaned_data['process'].process_name +" \"")
		return super(ActivitySwap, self).form_valid(form)


@login_required(login_url='/login')
def AssociateReferer(request, **kwargs):
	split = request.META.get('HTTP_REFERER').split("/")
	return HttpResponseRedirect("/processos/ProcessDetail/"+split[-1])

@login_required(login_url='/login')
def removePatternFromActivity(request, **kwargs):
	this_act = Activity.objects.filter(pk=kwargs['pk'])[0]
	this_pattern = Pattern.objects.filter(pk=kwargs['fk'])[0]
	this_act.pattern.remove(this_pattern)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))#previous URL

@login_required(login_url='/login')
def addPatternToActivity(request, **kwargs):
	this_act = Activity.objects.filter(pk=kwargs['pk'])[0]
	this_pattern = Pattern.objects.filter(pk=kwargs['fk'])[0]
	this_act.pattern.add(this_pattern)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ProcessCreate(CreateView):
	model = Process
	fields = ['process_name', 'user' , 'description']
	template_name = "processes/forms/process_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(ProcessCreate, self).get_form(form_class)
		form.fields['user'].widget = forms.HiddenInput()
		form.initial['user'] = self.request.user
		form.fields['process_name'].label = "Nome do Processo"
		form.fields['description'].label = "Descrição"
		return form 

	def form_valid(self, form):
		messages.info(self.request, f"Processo " +  " \""+ form.cleaned_data['process_name'] + f"\" inserido no sistema")
		return super(ProcessCreate, self).form_valid(form)

class ProcessUpdate(UpdateView):
	model = Process
	fields = ['process_name', 'description' , 'user']
	template_name = "processes/forms/process_update_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(ProcessUpdate, self).get_form(form_class)
		perm = Permission.objects.get(codename='test_GProc')  
		gp_users = User.objects.filter(groups__permissions=perm)
		form.fields['user'] = forms.ModelChoiceField(queryset=gp_users)
		form.fields['user'].empty_label = None
		form.fields['process_name'].label = "Nome do Processo"
		form.fields['description'].label = "Descrição"
		return form

	def form_valid(self, form):
		messages.info(self.request, f"Processo " +  " \""+ form.cleaned_data['process_name'] + f"\" alterado com sucesso")
		return super(ProcessUpdate, self).form_valid(form)

class ProcessDelete(DeleteView):
	model = Process
	sucess_url = "/processos"
	template_name = "processes/forms/process_confirm_delete.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		proc_id = self.object.id
		our_acts = Activity.objects.all().filter(process__id=proc_id)
		context['acts'] = our_acts
		return context
	def delete(self, request, *args, **kwargs):
		messages.warning(self.request,f"Processo " +  " \""+ Process.objects.filter(id=self.kwargs['pk'])[0].process_name+ f"\" apagado do sistema")
		return super(ProcessDelete, self).delete(request, *args, **kwargs)

class ProcessDetail(DetailView):
	model = Process
	template_name = "processes/forms/process_detail.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		proc_id = self.object.id
		context['pid'] = self.kwargs['pk']
		our_acts = Activity.objects.all().filter(process__id=proc_id)
		context['proc_acts'] = our_acts
		context['non_acts'] = Activity.objects.all().exclude(id__in=our_acts).exclude(process__isnull=False)
		return context

@login_required(login_url='/login')
def produtos(request):
	return render(request=request,
					template_name="processes/produtos.html",
					context={"users" : User.objects.all(),
					"groups" : Group.objects.all(),
					 "prods" : Product.objects.all() })




class ProductCreate(CreateView):
	model = Product
	fields = ['product_name', 'product_format', 'activity']
	template_name = "processes/forms/product_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(ProductCreate, self).get_form(form_class)
		#form.fields['user'].widget
		form.fields['activity'] = forms.ModelMultipleChoiceField(queryset=Activity.objects.all() ,widget=forms.CheckboxSelectMultiple())
		form.fields['product_name'].label = "Nome do produto"
		form.fields['product_format'].label = "Formato"
		form.fields['activity'].label = "Actividades"
		return form

	def form_valid(self, form):
		messages.info(self.request, f"Produto " +  " \""+ form.cleaned_data['product_name'] + f"\" inserido no sistema")
		return super(ProductCreate, self).form_valid(form)

class ProductDetail(DetailView):
	model = Product
	template_name = "processes/forms/product_detail.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		product_id = self.object.id
		context['pid'] = self.kwargs['pk']
		this_product = Product.objects.all().filter(id=product_id)[0]
		original_acts = Activity.objects.all().exclude(original__isnull=False)
		proc_acts = Activity.objects.all().exclude(original__isnull=True)
		our_acts = this_product.activity.all().exclude(id__in=proc_acts)
		our_proc_acts = this_product.activity.all().exclude(id__in=original_acts)
		context['acts'] = our_acts
		context['non_acts'] = original_acts.exclude(id__in=our_acts)
		context['proc_acts'] = our_proc_acts
		context['non_proc_acts'] = proc_acts.exclude(id__in=our_proc_acts)
		return context


class ProductUpdate(UpdateView):
	model = Product
	fields = ['product_name', 'product_format', 'activity']
	template_name = "processes/forms/product_update_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(ProductUpdate, self).get_form(form_class)
		#form.fields['user'].widget
		form.fields['activity'] = forms.ModelMultipleChoiceField(queryset=Activity.objects.all() ,widget=forms.CheckboxSelectMultiple())
		form.fields['product_name'].label = "Nome do produto"
		form.fields['product_format'].label = "Formato"
		form.fields['activity'].label = "Actividades"
		return form

	def form_valid(self, form):
		messages.info(self.request, f"Produto " +  " \""+ form.cleaned_data['product_name'] + f"\" alterado com sucesso")
		return super(ProductUpdate, self).form_valid(form)


class ProductDelete(DeleteView):
	model = Product
	sucess_url = "/produtos"
	template_name = "processes/forms/product_confirm_delete.html"
	def delete(self, request, *args, **kwargs):
		messages.warning(self.request,f"Produto " +  " \""+ Product.objects.filter(id=self.kwargs['pk'])[0].product_name+ f"\" apagado do sistema")
		return super(ProductDelete, self).delete(request, *args, **kwargs)

@login_required(login_url='/login')
def removeActivityFromProduct(request, **kwargs):
	this_product = Product.objects.filter(pk=kwargs['pk'])[0]
	this_act = Activity.objects.filter(pk=kwargs['fk'])[0]
	this_product.activity.remove(this_act)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))#previous URL

@login_required(login_url='/login')
def addActivityToProduct(request, **kwargs):
	this_product = Product.objects.filter(pk=kwargs['pk'])[0]
	this_act = Activity.objects.filter(pk=kwargs['fk'])[0]
	this_product.activity.add(this_act)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class RoleCreate(CreateView):
	model = Role
	fields = ['role_name' , 'description']
	template_name = "processes/forms/role_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(RoleCreate, self).get_form(form_class)
		#form.fields['user'].widget
		#form.fields['product'] = forms.ModelMultipleChoiceField(queryset=Product.objects.all() ,widget=forms.CheckboxSelectMultiple())
		form.fields['role_name'].label = "Nome do papel"
		form.fields['description'].label = "Descrição"
		return form

	def form_valid(self, form):
		messages.info(self.request, f"Papel " +  " \""+ form.cleaned_data['role_name'] + f"\" inserido no sistema")
		return super(RoleCreate, self).form_valid(form)

class RoleDetail(DetailView):
	model = Role
	template_name = "processes/forms/role_detail.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		role_id = self.object.id
		context['pid'] = self.kwargs['pk']
		this_rol = Role.objects.all().filter(id=role_id)[0]
		original_acts = Activity.objects.all().exclude(original__isnull=False)
		proc_acts = Activity.objects.all().exclude(original__isnull=True)
		our_acts = original_acts.filter(role__id=role_id)
		our_proc_acts = proc_acts.filter(role__id=role_id)
		context['acts'] = our_acts
		context['non_acts'] = original_acts.exclude(id__in=our_acts)
		context['proc_acts'] = our_proc_acts
		context['non_proc_acts'] = proc_acts.exclude(id__in=our_proc_acts)
		return context


class RoleUpdate(UpdateView):
	model = Role
	fields = ['role_name' , 'description']
	template_name = "processes/forms/role_update_form.html"
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		form = super(RoleUpdate, self).get_form(form_class)
		#form.fields['user'].widget
		#form.fields['product'] = forms.ModelMultipleChoiceField(queryset=Product.objects.all() ,widget=forms.CheckboxSelectMultiple())
		form.fields['role_name'].label = "Nome do papel"
		form.fields['description'].label = "Descrição"
		return form

	def form_valid(self, form):
		messages.info(self.request, f"Papel " +  " \""+ form.cleaned_data['role_name'] + f"\" alterado com sucesso")
		return super(RoleUpdate, self).form_valid(form)
		
class RoleDelete(DeleteView):
	model = Role
	sucess_url = "/papeis"
	template_name = "processes/forms/role_confirm_delete.html"
	def delete(self, request, *args, **kwargs):
		messages.warning(self.request,f"Papel " +  " \""+ Role.objects.filter(id=self.kwargs['pk'])[0].role_name+ f"\" apagado do sistema")
		return super(RoleDelete, self).delete(request, *args, **kwargs)

@login_required(login_url='/login')
def removeRoleFromActivity(request, **kwargs):
	this_act = Activity.objects.filter(pk=kwargs['pk'])[0]
	this_rol = Role.objects.filter(pk=kwargs['fk'])[0]
	this_act.role.remove(this_rol)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))#previous URL

@login_required(login_url='/login')
def addRoleToActivity(request, **kwargs):
	this_act = Activity.objects.filter(pk=kwargs['pk'])[0]
	this_rol = Role.objects.filter(pk=kwargs['fk'])[0]
	this_act.role.add(this_rol)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def home(request):
	return render(request=request,
				  template_name="processes/homepage.html",
				   context={"procs": Process.objects.all(), "acts": Activity.objects.all().exclude(original__isnull=False),
				   			"roles": Role.objects.all()	, "users" : User.objects.all(),	
							 "orgs" : Organization.objects.all(), "prods" : Product.objects.all(),							
							"proc_acts": Activity.objects.filter(process__user=request.user) 
				   }
				   )

@login_required(login_url='/login')
def papeis(request):
	return render(request=request,
				  template_name="processes/papeis.html",
				   context={"procs": Process.objects.all(), "acts": Activity.objects.all(),
				   			"roles": Role.objects.all()	, "users" : User.objects.all(),	
							  "prods" : Product.objects.all(),							
				   }
				   )




class ViewProcess(AjaxableResponseMixin,DetailView):
	model = Process
	template_name = "processes/modal/process.html"



class ViewPattern(AjaxableResponseMixin,DetailView):
	model = Pattern
	template_name = "processes/modal/pattern.html"

	
class ViewRole(AjaxableResponseMixin,DetailView):
	model = Role
	template_name = "processes/modal/role.html"

class ViewActivity(AjaxableResponseMixin,DetailView):
	model = Activity
	template_name = "processes/modal/activity.html"	

class ViewProduct(AjaxableResponseMixin,DetailView):
	model = Product
	template_name = "processes/modal/product.html"
