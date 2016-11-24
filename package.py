def packages(options,front,data_f,data_h,av,budget,adult,children,interval):

    result_list = []
    total_list = []
    for i in range(len(front)):
        for option in options:

            if int(option['key']) == int(front[i]):
                result_list.append(option['name'])
    print(result_list)
    print(data_f)
    print(data_h)
    print(options)
    # compare with budget using flight_price and room_price
    budgetlist= []
    for b in range(len(result_list)):
        for option in options:
            # print(str(result_list[b]))
            # print(option['name'])
            if str(option['name'])==str(result_list[b]):
                print('yes')
                priceF=option['values']['flight_price']
                priceH=option['values']['room_price']
                num=int((adult+children)/2)+1
                total=float(priceF+priceH*num*interval)
                total_list.append(total)
                print(total)
                print(budget)
                if total<=budget:
                    print('add')
                    print(result_list[b])
                    budgetlist.append(result_list[b])

    print("budget list:{} and length {} ".format(budgetlist,len(budgetlist)))
    print("Total list:{} ".format(total_list))
    results= []
    if len(budgetlist)==0:
        print("Inside budget list is zero")
        minTot = min(total_list)
        errorDict = {}
        errorDict["Error"] = "Minimum budget should be: " + str(minTot)
        results.append(errorDict)
        print("min budget:{} ".format(results))
        return  results
    else:
        print("budget list is not zero")
    for k in range(len(budgetlist)):
        a=budgetlist[k].split(',')
        flight=int(a[0][-1:])
        hotel=int(a[1][-1:])
        f=data_f[flight-1]
        h=data_h[hotel-1]

        hotel_package={a[1][:-1]:h}
        package = f.copy()
        package.update(hotel_package)
        all = package.copy()
        all.update(av)
        results.append(all)

    return(results)




