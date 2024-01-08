
class Sequentiality:
  def __init__(self):
     pass

  def find_LongestConseqSubseq(self,arr):
     
      n=len(arr)
      ans = 0
      count = 0
      arr.sort()
      v = []

      v.append(arr[0])

      for i in range(1, n):
          if (arr[i] != arr[i - 1]):
              v.append(arr[i])

      # Find  max length by traversing the array
      for i in range(len(v)):
        #  if the current element is equal to previous element +1
        if (i > 0 and v[i] == v[i - 1] + 1):
          count += 1
        # Reset the count
        else:
          count = 1
        ans = max(ans, count)

      return ans


  def find_LongestConseqSubseq_1gap(self,arr):
    
    _ , locs=self.find_sequential_elements_with_difference_of_2(arr)

    if len(locs)>0:

      results=[]
      for i in range(len(arr)):


          temp=arr.copy()
          if i in locs:

            temp.insert(i+1,temp[i]+1 )

            #  r=calculate_LCS_m(temp)
            r=self.find_LongestConseqSubseq(temp)
            results.append(r)

      return max(results)

    else:

      r=self.find_LongestConseqSubseq(arr)
      return r


  def find_LongestConseqSubseq_2gap(self,arr):

    _ , locs=self.find_sequential_elements_with_difference_of_3(arr)

    if len(locs)>0:

      results=[]
      for i in range(len(arr)):
          # print("i:",i)

          temp=arr.copy()
          if i in locs:
            # print("i in locs")
            # print(temp)
            temp.insert(i+1,temp[i]+1 )
            temp.insert(i+2,temp[i]+2 )
            # print(temp)
            #  r=calculate_LCS_m(temp)
            r=self.find_LongestConseqSubseq(temp)
            results.append(r)

      return max(results)

    else:

        r= self.find_LongestConseqSubseq_1gap(arr)
    return r

  def find_LongestConseqSubseq_from_end(self, arr):
     
      rg=range(len(arr) - 1 , -1, -1)
      current_length = 1
      for i in rg:
        if arr[i] - 1 == arr[i - 1]:
              current_length += 1
        else:
          break
      return current_length


  def find_LongestConseqSubseq_from_end_with_1_gap(self,arr):
      rg=range(len(arr) - 1 , -1, -1)
      current_length = 1
      one_time_flag=False
      for i in rg:
        if arr[i] - 1 == arr[i - 1]:
              current_length += 1
        elif arr[i] - 2 == arr[i - 1]:
          if one_time_flag==False:
            current_length += 1
            one_time_flag=True
        else:
          break
      return current_length



  def find_LongestConseqSubseq_from_end_with_2_gap(self,arr):
     
      rg=range(len(arr) - 1 , -1, -1)
      current_length = 1
      two_time_flag=0
      for i in rg:
        if arr[i] - 1 == arr[i - 1]:
              current_length += 1

        elif arr[i] - 2 == arr[i - 1]:
            if not two_time_flag  >2:
              current_length += 1
              two_time_flag+= 1
              if two_time_flag==2:
                  two_time_flag+= 1
        elif arr[i] - 3 == arr[i - 1]:
            if two_time_flag==0:
              current_length += 1
              two_time_flag=3

      return current_length


  def find_sequential_elements_with_difference_of_2(self,sequence):
    sequential_pairs = []
    locs = []
    for i in range(len(sequence) - 1):
        if sequence[i + 1] - sequence[i] == 2:
            sequential_pairs.append((sequence[i], sequence[i + 1]))
            locs.append(i)
    return sequential_pairs, locs


  def find_sequential_elements_with_difference_of_3(self,sequence):
      sequential_pairs = []
      locs = []
      for i in range(len(sequence) - 1):
          if sequence[i + 1] - sequence[i] == 3:
              sequential_pairs.append((sequence[i], sequence[i + 1]))
              locs.append(i)
      return sequential_pairs, locs
