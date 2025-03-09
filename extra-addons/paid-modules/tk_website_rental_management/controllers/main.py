# -*- coding: utf-8 -*-
# Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import http, _
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


def category_wise_domain_filter(list_type):
    """Category wise domain filter for property"""
    list_domain = []
    if list_type and list_type == 'lands':
        list_domain.append(('type', '=', 'land'))
    if list_type and list_type == 'apartments':
        list_domain.append(('residence_type', '=', 'apartment'))
    if list_type and list_type == 'houses':
        list_domain.append(('residence_type', 'in', ['bungalow', 'vila', 'raw_house', 'duplex', 'single_studio']))
    if list_type and list_type == 'industrials':
        list_domain.append(('type', '=', 'industrial'))
    if list_type and list_type == 'commercials':
        list_domain.append(('type', '=', 'commercial'))
    return list_domain


def get_amenities_filters(param):
    """Amenities wise domain filter of property"""
    url_args, list_domain = dict(), []
    # Amenities filter - gym
    web_gym = param.get('gym')
    if web_gym and web_gym == '1':
        url_args['gym'] = '1'
        list_domain.append(('web_gym', '=', True))
    # wifi
    web_wifi = param.get('wifi')
    if web_wifi and web_wifi == '1':
        url_args['gym'] = '1'
        list_domain.append(('web_wifi', '=', True))
    # parking
    web_parking = param.get('parking')
    if web_parking and web_parking == '1':
        url_args['parking'] = '1'
        list_domain.append(('web_parking', '=', True))
    # pool
    web_pool = param.get('pool')
    if web_pool and web_pool == '1':
        url_args['pool'] = '1'
        list_domain.append(('web_pool', '=', True))
    # security
    web_security = param.get('security')
    if web_security and web_security == '1':
        url_args['security'] = '1'
        list_domain.append(('web_security', '=', True))
    # laundry
    web_laundry = param.get('laundry')
    if web_pool and web_laundry == '1':
        web_laundry['laundry'] = '1'
        list_domain.append(('web_laundry', '=', True))
    # Equipped Kitchen
    web_equip_kitchen = param.get('kitchen')
    if web_equip_kitchen and web_equip_kitchen == '1':
        url_args['kitchen'] = '1'
        list_domain.append(('web_equip_kitchen', '=', True))
    # Equipped Kitchen
    web_equip_kitchen = param.get('kitchen')
    if web_equip_kitchen and web_equip_kitchen == '1':
        url_args['kitchen'] = '1'
        list_domain.append(('web_equip_kitchen', '=', True))
    # AC
    web_air_condition = param.get('ac')
    if web_air_condition and web_air_condition == '1':
        url_args['ac'] = '1'
        list_domain.append(('web_air_condition', '=', True))
    # semi furnish
    web_semi_furnish = param.get('smf')
    if web_semi_furnish and web_semi_furnish == '1':
        url_args['smf'] = '1'
        list_domain.append(('web_semi_furnish', '=', True))
    # full furnish
    web_full_furnish = param.get('fuf')
    if web_full_furnish and web_full_furnish == '1':
        url_args['fuf'] = '1'
        list_domain.append(('web_full_furnish', '=', True))
    # Alarm
    web_alarm = param.get('alarm')
    if web_alarm and web_alarm == '1':
        url_args['alarm'] = '1'
        list_domain.append(('web_alarm', '=', True))
    # window cover
    web_window_cover = param.get('wc')
    if web_window_cover and web_window_cover == '1':
        url_args['wc'] = '1'
        list_domain.append(('web_window_cover', '=', True))

    return url_args, list_domain


def property_filters(param):
    """Get all filters together"""
    url_args, list_domain = dict(), []
    # status filters
    status = param.get('st')
    if status and status in ['sale', 'rent']:
        url_args['st'] = status
        if status == 'sale':
            list_domain.append(('sale_lease', '=', 'for_sale'))
        else:
            list_domain.append(('sale_lease', '=', 'for_tenancy'))

        # price range filters - starting price
        price_start = param.get('price-start')
        if price_start and price_start.isdigit():
            if status == 'sale':
                url_args['price-start'] = price_start
                list_domain.append(('sale_price', '>=', int(price_start)))
            else:
                list_domain.append(('tenancy_price', '>=', int(price_start)))
        # price range filters - ending price
        price_end = param.get('price-end')
        if price_end and price_end.isdigit():
            url_args['price-end'] = price_end
            if status == 'sale':
                list_domain.append(('sale_price', '<=', int(price_end)))
            else:
                list_domain.append(('tenancy_price', '<=', int(price_end)))

    # city filters
    city = request.params.get('c')
    if city and 'All' not in city:
        cities = request.env['property.res.city'].sudo().search([('name', '=', str(city))]).ids
        if cities:
            url_args['c'] = city
            list_domain.append(('city_id', 'in', cities))

    # category filters
    categ = param.get('categ')
    if categ and len(categ) > 0 and 'All' not in categ:
        url_args['categ'] = categ
        list_domain = list_domain + category_wise_domain_filter(categ)

        # area filters
        area_start = param.get('area-start')
        area_end = param.get('area-end')
        if area_start and area_start.isdigit() and area_end and area_end.isdigit():
            url_args['area-start'] = area_start
            url_args['area-end'] = area_end
            if categ in ('apartments', 'houses'):
                list_domain.append(('total_square_ft', '>=', int(area_start)),
                                   ('total_square_ft', '<=', int(area_end)))
            elif categ == 'industrials':
                list_domain.append(('total_industrial_measure', '>=', int(area_start)),
                                   ('total_industrial_measure', '<=', int(area_end)))
            elif categ == 'commercials':
                list_domain.append(('total_commercial_measure', '>=', int(area_start)),
                                   ('total_commercial_measure', '<=', int(area_end)))
            elif categ == 'lands':
                list_domain.append(('area_hector', '>=', int(area_start)),
                                   ('area_hector', '<=', int(area_end)))

    # max price filters
    max_price = param.get('mx_prc')
    if max_price and max_price.isdigit():
        url_args['mx_prc'] = max_price
        list_domain.append(('tenancy_price', '<=', int(max_price)))
        list_domain.append(('sale_price', '<=', int(max_price)))

    # search term filters
    search_term = param.get('search_term')
    if search_term:
        url_args['search_term'] = search_term
        list_domain.append(('name', 'ilike', search_term))

    return url_args, list_domain


def property_sorting_orders(param):
    """Sorting order of property records"""
    url_args, default_order = dict(), ""
    # Property type sort filter
    property_type = param.get('property_type')
    if property_type and property_type in ['sale', 'rent']:
        url_args['property_type'] = property_type
        if property_type == 'sale':
            default_order = 'sale_lease ASC'
        else:
            default_order = 'sale_lease DESC'
    else:
        default_order = 'id DESC'
    # Price order sort filter
    price_order = param.get('price_order')
    if price_order and property_type and property_type in ('sale', 'rent') and price_order in ('lh', 'hl'):
        url_args['price_order'] = price_order
        if price_order == 'lh':
            default_order += ',' + 'tenancy_price ASC' if property_type == 'rent' else ',' + 'sale_price ASC'
        else:
            default_order += ',' + 'tenancy_price DESC' if property_type == 'rent' else ',' + 'sale_price DESC'
    return url_args, default_order


def get_all_filters(param):
    """Combine filters & Sorting orders"""
    # query param args
    url_args, list_domain = dict(), []

    # sorting orders
    sort_args, default_order = property_sorting_orders(param)
    url_args.update(sort_args)

    # property filters
    filter_args, prop_list_domain = property_filters(param)
    url_args.update(filter_args)
    list_domain = list_domain + prop_list_domain

    # amenities filters
    ame_args, ame_filters = get_amenities_filters(param)
    url_args.update(ame_args)
    list_domain = list_domain + ame_filters

    return url_args, list_domain, default_order


class PropertyController(Website):
    """Property website"""

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        """Home page of property management"""
        # theme config rec
        home_config = request.env.ref('tk_website_rental_management.property_theme_config_rec')
        # property details env
        property_param = request.env['property.details'].sudo()
        # latest listing
        latest_listing = property_param.search([('stage', '=', 'available')], order='id desc',
                                               limit=home_config.no_latest_list)
        # popular listing
        popular_listing = property_param.search([('stage', '=', 'available'), ('is_popular_list', '=', True)],
                                                order='id desc', limit=home_config.no_popular_list)

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids
        ctx = {
            'latest_listing': latest_listing,
            'popular_listing': popular_listing,
            'home_config': home_config,
            'book_properties': book_prop,
            'book_property_count': len(book_prop),
            'cities': property_param.get_all_cities(),
        }
        return request.render("tk_website_rental_management.homes", ctx)

    @http.route(['/properties-list',
                 '/properties-list/page/<int:page>',
                 '/properties-list/<string:list_type>',
                 '/properties-list/<string:list_type>/page/<int:page>'], type='http', auth="public", website=True)
    def properties_list(self, list_type=None, page=0, **kw):
        """List of properties"""
        property_param = request.env['property.details'].sudo()
        # theme config rec
        config_rec = request.env.ref('tk_website_rental_management.property_theme_config_rec')
        # domain list
        list_domain = [('stage', '=', 'available')]
        # category wise filter domain
        if list_type:
            list_domain = list_domain + category_wise_domain_filter(list_type)

        # Property filters
        url_args, prop_filters, default_order = get_all_filters(request.params)
        list_domain = list_domain + prop_filters

        # property list limit
        property_per_page = config_rec.list_property_per_page
        list_count = property_param.search_count(list_domain)

        # pagination
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=list_count,
            page=page,
            step=property_per_page,
            url_args=url_args,
        )
        # listings
        listing = property_param.search(list_domain, order=default_order, offset=pager['offset'],
                                        limit=property_per_page)

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids
        ctx = {
            'listing': listing,
            'list_type': list_type,
            'pager': pager,
            'cities': property_param.get_all_cities(),
            'theme_config': config_rec,
            'book_properties': book_prop,
            'book_property_count': len(book_prop),
        }
        return request.render("tk_website_rental_management.property_list", ctx)

    @http.route(['/properties/city/<model("property.res.city"):city>/',
                 '/properties/city/<model("property.res.city"):city>/page/<int:page>'], type='http', auth="public",
                website=True)
    def properties_list_by_city(self, city, page=0):
        """City wise property list"""
        # theme config rec
        config_rec = request.env.ref('tk_website_rental_management.property_theme_config_rec')
        property_param = request.env['property.details'].sudo()
        # domain list city wise
        list_domain = [('stage', '=', 'available'), ('city_id', '=', city.id)]

        # Property filters
        url_args, prop_filters, default_order = get_all_filters(request.params)
        list_domain = list_domain + prop_filters

        # limit per page
        property_per_page = config_rec.list_property_per_page
        list_count = property_param.search_count(list_domain)

        # Pagination
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=list_count,
            page=page,
            step=property_per_page,
            url_args=url_args,
        )
        listing = property_param.search(list_domain, order=default_order, offset=pager['offset'],
                                        limit=property_per_page)

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids
        ctx = {
            'listing': listing,
            'pager': pager,
            'city': city,
            'cities': property_param.get_all_cities(),
            'theme_config': config_rec,
            'book_properties': book_prop,
            'book_property_count': len(book_prop),
        }
        return request.render("tk_website_rental_management.property_list", ctx)

    @http.route('/property-details/<model("property.details"):prop>', type='http', auth="public", website=True)
    def property_details(self, prop, **kw):
        """Get single property details"""
        error_msg, enquiry_made = False, False
        if request.httprequest.method == 'POST':
            # Enquiry form validation
            if not kw.get('name'):
                error_msg = 'Name is required'
            if not kw.get('email'):
                error_msg = 'Email is required'
            if not kw.get('mobile'):
                error_msg = 'Mobile is required'
            # Create lead
            if not error_msg:
                lead_data = {
                    'name': prop.name + " " + kw.get('name', ''),
                    'contact_name': kw.get('name', ''),
                    'email_from': kw.get('email', ''),
                    'mobile': kw.get('mobile', ''),
                    'description': kw.get('additional_details', ''),
                    'partner_id': request.env.user.partner_id.id,
                    'property_id': prop.id,
                }
                request.env['crm.lead'].sudo().create(lead_data)
        # Find booked properties
        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids
        # Check already enquiry is submitted or not
        if request.env.user.id != request.env.ref('base.public_user').id:
            lead = request.env['crm.lead'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id), ('property_id', '=', prop.id)])
            if lead:
                enquiry_made = True
        # No of bookmarks
        bookmark_count = request.env['property.bookmark'].sudo().search_count([('property_id', '=', prop.id)])
        # context
        ctx = {
            'prop': prop,
            'book_properties': book_prop,
            'error_msg': error_msg,
            'enquiry_made': enquiry_made,
            'book_count': bookmark_count,
        }
        return request.render("tk_website_rental_management.property_details", ctx)

    @http.route('/property/wishlist', type='json', auth="user")
    def property_wishlist(self, **kw):
        """User wise wishlist of different property"""
        bookmark_param = request.env['property.bookmark'].sudo()
        property_id = request.env['property.details'].sudo().search([('access_token', '=', kw.get('access'))],
                                                                    limit=1).id
        if property_id:
            toggle = kw.get('toggle')
            bookmark_property = bookmark_param.search([('property_id', '=', property_id),
                                                       ('partner_id', '=',
                                                        request.env.user.partner_id.id)],
                                                      limit=1)
            if toggle and bookmark_property:
                bookmark_property.unlink()
            else:
                bookmark_param.create({'property_id': property_id, 'partner_id': request.env.user.partner_id.id})

        book_prop = bookmark_param.search_count(
            [('partner_id', '=', request.env.user.partner_id.id)])
        return {'count': book_prop}

    @http.route('/property/wishlist/clear', type='json', auth="user")
    def property_wishlist_clear(self, **kw):
        """Clear wishlist of property"""
        bookmark_param = request.env['property.bookmark'].sudo()
        property_id = request.env['property.details'].sudo().search([('access_token', '=', kw.get('access'))],
                                                                    limit=1).id
        if property_id:
            bookmark_property = bookmark_param.search([('property_id', '=', property_id),
                                                       ('partner_id', '=',
                                                        request.env.user.partner_id.id)],
                                                      limit=1)
            if bookmark_property:
                bookmark_property.unlink()
        book_prop = bookmark_param.search_count([('partner_id', '=', request.env.user.partner_id.id)])
        return {'count': book_prop - 1}


class PropertyCustomerPortal(CustomerPortal):
    """Customer portal entry for property enquiry"""
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        enquiries = request.env['crm.lead']
        domain = [('partner_id', '=', request.env.user.partner_id.id), ('property_id', '!=', False)]
        values['enquiry_count'] = enquiries.search_count(domain)
        return values

    @http.route(['/property/enquiries'], type='http', auth="user", website=True)
    def property_enquiry_details(self):
        """Get list of property enquiries"""
        enquiries = request.env['crm.lead'].sudo()
        domain = [('partner_id', '=', request.env.user.partner_id.id), ('property_id', '!=', False)]
        recs = enquiries.search(domain)
        ctx = {
            'enqs': recs,
            'page_name': 'enquiry',
        }
        return request.render("tk_website_rental_management.enquiry_list", ctx)

    @http.route(['/property/enquiry/details/<model("crm.lead"):enquiry>'], type='http', auth="user", website=True)
    def portal_my_enquiry_detail(self, enquiry):
        """Return enquiry by property"""
        ctx = {
            'enquiry': enquiry,
            'page_name': 'enquiry',
        }
        return request.render("tk_website_rental_management.enquiry_details", ctx)
