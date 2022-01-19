
content = 'This is a #test #wow #kkk'
htag = '#'
arr = content.split()

keyword_list = []


for i in range(len(arr)):
    if '#' in arr[i]:
        keyword_list.append(arr[i]) 
        
print (keyword_list)

#검색 결과 페이지로 해쉬태그 창 띄우기


# api.add_resource(Search, '/search/<str:keyword_list[?]>')
# feeds.query.filter(Feeds.content.like(f"%{keyword}%")).all()

#검색 결과 줄임표 가공
# content = 'awegawepg awjpegj pawegj #keyword awgpawp egjapwe jpgajagwjp'
# content_short = content