import itertools

import numpy as np
from PIL import Image, ImageDraw


class SeamCarving:
    def __init__(self, path, mode=1):
        self.path = path
        self.mode = mode
        self.image = Image.open(self.path)

    def find_energy(self):
        image = self.image
        img_height = image.height
        img_width = image.width
        energy = np.zeros((img_width, img_height))
        image_np = np.asarray(image, dtype='uint8')

        print(img_width)
        print(img_height)
        print(len(image_np))
        print(len(image_np[0]))

        for i in range(img_width):
            for j in range(img_height):
                energy[i][j] = 0

                for k in range(3):
                    summ = 0
                    count = 0

                    if i != img_width - 1:
                        count += 1
                        summ += abs(image.getpixel((i, j))[k] - image.getpixel((i + 1, j))[k])
                        # summ += abs(image_np[j, i, k] - image_np[j, i + 1, k])
                        # print(image_np[i, j, k], image.getpixel((i, j))[k])

                    if j != img_height - 1:
                        count += 1
                        summ += abs(image.getpixel((i, j))[k] - image.getpixel((i, j + 1))[k])

                    if count != 0:
                        energy[i][j] += summ // count
        return energy

    def draw_energy(self):
        offs = 255 * bool(self.mode)
        energy = self.find_energy()
        x = len(energy)
        y = len(energy[0])
        # ImageDraw.Draw('RGB', (x, y)).point((i, j), fill=img.getpixel(xy))
        im = Image.new('RGB', (x, y))
        draw = ImageDraw.Draw(im)
        for i, j in itertools.product(range(x), range(y)):
            # draw.point((i, j), fill=(int(energy[i][j]), int(energy[i][j]), int(energy[i][j]), int(energy[i][j])))
            draw.point((i, j), fill=(abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j]))))
        print('redy')
        im.save(self.path, format='png')

        return self.path

    def show_energy(self):
        offs = 255 * bool(self.mode)
        energy = self.find_energy()
        x = len(energy)
        y = len(energy[0])
        # ImageDraw.Draw('RGB', (x, y)).point((i, j), fill=img.getpixel(xy))
        im = Image.new('RGB', (x, y))
        draw = ImageDraw.Draw(im)
        for i, j in itertools.product(range(x), range(y)):
            # draw.point((i, j), fill=(int(energy[i][j]), int(energy[i][j]), int(energy[i][j]), int(energy[i][j])))
            draw.point((i, j), fill=(abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j]))))
        print('redy')

        return im.show()

    def find_sum(self, mode='x'):
        image = self.image
        img_height = image.height
        img_width = image.width
        energy = self.find_energy()
        summm = [[0 for _ in range(img_height)] for __ in range(img_width)]
        # summm = energy

        # y
        # for j in range(img_height):
        #     summm[0][j] = energy[0][j]
        for i in range(img_width):
            summm[i][0] = energy[i][0]

        # energy[i,j] + MIN ( sum[i-1, j-1], sum[i-1, j], sum[i-1, j+1])
        # y
        # for i in range(1, img_width):
        #     for j in range(img_height):
        #         summm[i][j] = summm[i - 1][j]
        #         if j > 0 and summm[i - 1][j - 1] < summm[i][j]:
        #             summm[i][j] = summm[i - 1][j - 1]
        #         if j < img_height - 1 and summm[i - 1][j + 1] < summm[i][j]:
        #             summm[i][j] = summm[i - 1][j + 1]
        #         summm[i][j] += energy[i][j]
        # print(len(summm), len(summm[0]))
        for j in range(1, img_height):
            for i in range(img_width):
                summm[i][j] = summm[i][j - 1]
                # print(i, j)
                # print(summm[i][j])
                # if i > 0:
                #     print(summm[i-1][j-1])
                # if i < img_width - 1:
                #     print(summm[i+1][j-1])
                if i > 0 and summm[i - 1][j - 1] < summm[i][j]:
                    summm[i][j] = summm[i - 1][j - 1]
                if i < img_width - 1 and summm[i + 1][j - 1] < summm[i][j]:
                    summm[i][j] = summm[i + 1][j - 1]
                # print(summm[i][j])
                # print('---')
                summm[i][j] += energy[i][j]
        return summm

    def find_shrinked_pixels(self):
        image = self.image
        img_height = image.height
        img_width = image.width
        summm = self.find_sum()
        x = len(summm)
        y = len(summm[0])
        last = img_height - 1

        res = [0 for _ in range(img_height)]

        res[last] = 0
        for i in range(1, img_width):
            if summm[i][last] < summm[res[last]][last]:
                res[last] = i

        for j in range(last-1, -1, -1):
            prev = int(res[j + 1])

            res[j] = prev
            if prev > 0 and summm[res[j]][j] > summm[prev - 1][j]:
                res[j] = prev - 1
            if prev < img_width - 1 and summm[res[j]][j] > summm[prev + 1][j]:
                res[j] = prev + 1
        return res

    def find_shrinked_pixels_alt(self):
        image = self.image
        img_height = image.height
        img_width = image.width
        summm = self.find_sum()
        x = len(summm)
        y = len(summm[0])
        last = img_height - 1

        res = [0 for _ in range(img_height)]

        res[last] = 0
        for i in range(1, img_width):
            if summm[i][last] > summm[res[last]][last]:
                res[last] = i

        for j in range(last-1, -1, -1):
            prev = int(res[j + 1])

            res[j] = prev
            if prev > 0 and summm[res[j]][j] < summm[prev - 1][j]:
                res[j] = prev - 1
            if prev < img_width - 1 and summm[res[j]][j] < summm[prev + 1][j]:
                res[j] = prev + 1
        return res

    def _show_shrinked_pixels(self):
        image = self.image
        offs = 255 * bool(self.mode)
        res = self.find_shrinked_pixels()
        x = image.width
        y = image.height
        draw = ImageDraw.Draw(image)
        for j in range(y):
            # draw.point((i, j), fill=(int(energy[i][j]), int(energy[i][j]), int(energy[i][j]), int(energy[i][j])))
            # print(j)
            # if j != 0:
            # print(j)
            draw.point((res[j], j), fill=(255, 0, 0))
        print('redy')

        return image.show()

    def remove_lines(self, percentage=50):
        image = self.image
        times = image.width // 100 * percentage
        for time in range(times):
            image = self.image
            print(f'{time+1}/{times}')
            res = self.find_shrinked_pixels()
            x, y = self.image.size
            self.image = Image.new('RGBA', (x-1, y))
            draw = ImageDraw.Draw(self.image)
            get = 0
            for j in range(y):
                for i in range(x-1):
                    if i == res[j]:
                        # draw.point((i, j), fill=(255, 0, 0))
                        # continue
                        get = 1
                    draw.point((i, j), fill=image.getpixel((i+get, j)))
                get = 0


        print('redy')
        self.image.show()
        return self.image.save('test2.png')

    def _show_sum(self):
        offs = 255 * bool(self.mode)
        energy = self.find_sum()
        x = len(energy)
        y = len(energy[0])
        print(max(max(energy)))
        # ImageDraw.Draw('RGB', (x, y)).point((i, j), fill=img.getpixel(xy))
        im = Image.new('RGB', (x, y))
        draw = ImageDraw.Draw(im)
        for i, j in itertools.product(range(x), range(y)):
            # draw.point((i, j), fill=(int(energy[i][j]), int(energy[i][j]), int(energy[i][j]), int(energy[i][j])))
            # print(energy[i][j])
            # draw.point((i, j), fill=(255, 0, 0))
            # continue
            draw.point((i, j), fill=(abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j])), abs(offs - int(energy[i][j]))))

        print('redy')
        return im.show()


if __name__ == '__main__':
    picture = SeamCarving('test.jpg')
    picture.show_energy()
    picture._show_sum()
    picture._show_shrinked_pixels()

    # picture.remove_lines(percentage=10)
    # picture.remove_lines_alt(50)
    # TODO numba acceleration
